import React, { useState, useEffect, FC } from 'react';
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
  const { logout, token } = useAuth();

  useEffect(() => {
    if (!token) return;
    const fetchRecipes = async () => {
      try {
        setLoading(true);
        const data = await api.get<RecipeSummary[]>('/api/recipes/', token);
        setRecipes(data);
      } catch (err) {
        setError('Failed to load recipes.');
      } finally {
        setLoading(false);
      }
    };
    fetchRecipes();
  }, [token]);

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
              setRecipes(recipes.filter(r => r.id !== id));
          } catch (error) {
              console.error("Failed to delete recipe", error);
              alert("Failed to delete recipe.");
          }
      }
  }

  return (
    <div>
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800">My Recipes</h1>
        <div>
          <button onClick={() => { setView('form'); }} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg mr-4">+ New Recipe</button>
          <button onClick={logout} className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg">Logout</button>
        </div>
      </header>
      {loading && <Spinner />}
      {error && <ErrorMessage message={error} />}
      {!loading && !error && (
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
    </div>
  );
};
