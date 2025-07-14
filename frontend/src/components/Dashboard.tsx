import React, { useState, useEffect, FC, useCallback } from 'react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../services/api';
import { Recipe, RecipeSummary } from '../types';
import { Spinner } from './Spinner';
import { ErrorMessage } from './ErrorMessage';

type View = 'dashboard' | 'detail' | 'form';

interface DashboardProps {
    setView: (view: View) => void;
    setSelectedRecipeId: (id: number) => void;
    setRecipeToEdit: (recipe: Recipe) => void;
}

export const Dashboard: FC<DashboardProps> = ({ setView, setSelectedRecipeId, setRecipeToEdit }) => {
  const [recipes, setRecipes] = useState<RecipeSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState(''); // State for the search term
  const { logout, token } = useAuth();

  // useCallback helps prevent re-creating the function on every render
  const fetchRecipes = useCallback(async (searchQuery: string) => {
    if (!token) return;
    try {
      setLoading(true);
      // Append search query to the API call
      const url = searchQuery ? `/api/recipes/?search=${searchQuery}` : '/api/recipes/';
      const data = await api.get<RecipeSummary[]>(url, token);
      setRecipes(data);
    } catch (err) {
      setError('Failed to load recipes.');
    } finally {
      setLoading(false);
    }
  }, [token]);

  // useEffect for initial fetch and re-fetching on search term change
  useEffect(() => {
    // Debounce search to avoid API calls on every keystroke
    const delayDebounceFn = setTimeout(() => {
      fetchRecipes(searchTerm);
    }, 300); // 300ms delay

    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm, fetchRecipes]);

  const handleSelectRecipe = (id: number) => {
    setSelectedRecipeId(id);
    setView('detail');
  };

  const handleEdit = (recipeSummary: RecipeSummary) => {
    if(!token) return;
    api.get<Recipe>(`/api/recipes/${recipeSummary.id}/`, token).then(fullRecipe => {
        setRecipeToEdit(fullRecipe);
        setView('form');
    });
  }
  
  const handleDelete = async (id: number) => {
      if (!token) return;
      if (window.confirm("Are you sure you want to delete this recipe?")) {
          try {
              await api.delete(`/api/recipes/${id}/`, token);
              // Refetch recipes after deletion to show updated list
              fetchRecipes(searchTerm);
          } catch (error) {
              console.error("Failed to delete recipe", error);
              alert("Failed to delete recipe.");
          }
      }
  }

  return (
    <div>
      <header className="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
        <h1 className="text-4xl font-bold text-gray-800">My Recipes</h1>
        <div className="flex items-center gap-4">
          <button onClick={() => { setView('form'); }} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg whitespace-nowrap">+ New Recipe</button>
          <button onClick={logout} className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg">Logout</button>
        </div>
      </header>
      
      {/* Search Bar */}
      <div className="mb-6">
        <input 
          type="text"
          placeholder="Search by title or ingredient..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {loading && <Spinner />}
      {error && <ErrorMessage message={error} />}
      {!loading && !error && recipes.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {recipes.map(recipe => (
            <div key={recipe.id} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
              <div className="p-6">
                <div className="uppercase tracking-wide text-sm text-indigo-500 font-semibold">{recipe.yield_amount}</div>
                <a href="#" onClick={(e) => { e.preventDefault(); handleSelectRecipe(recipe.id); }} className="block mt-1 text-lg leading-tight font-medium text-black hover:underline">{recipe.title}</a>
                <div className="mt-4 flex justify-end gap-2">
                    <button onClick={() => handleSelectRecipe(recipe.id)} className="text-sm bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-1 px-3 rounded-lg">View</button>
                    <button onClick={() => handleEdit(recipe)} className="text-sm bg-blue-100 hover:bg-blue-200 text-blue-800 font-semibold py-1 px-3 rounded-lg">Edit</button>
                    <button onClick={() => handleDelete(recipe.id)} className="text-sm bg-red-100 hover:bg-red-200 text-red-800 font-semibold py-1 px-3 rounded-lg">Delete</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      {!loading && !error && recipes.length === 0 && (
          <div className="text-center py-12 bg-white rounded-lg shadow-md">
              <h3 className="text-xl font-semibold text-gray-700">No Recipes Found</h3>
              <p className="text-gray-500 mt-2">
                  {searchTerm ? "Try adjusting your search." : "Why not create a new recipe?"}
              </p>
          </div>
      )}
    </div>
  );
};