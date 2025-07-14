import React, { useState, useEffect, FC } from 'react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../services/api';
import { Recipe } from '../types';
import { Spinner } from './Spinner';
import { ErrorMessage } from './ErrorMessage';

interface RecipeDetailProps {
  recipeId: number;
  onBack: () => void;
  onEdit: (recipe: Recipe) => void;
}

export const RecipeDetail: FC<RecipeDetailProps> = ({ recipeId, onBack, onEdit }) => {
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { token } = useAuth();

  useEffect(() => {
    if (!token) return;
    const fetchRecipe = async () => {
      try {
        setLoading(true);
        const data = await api.get<Recipe>(`/api/recipes/${recipeId}/`, token);
        setRecipe(data);
      } catch (err) {
        setError('Failed to load recipe details.');
      } finally {
        setLoading(false);
      }
    };
    fetchRecipe();
  }, [recipeId, token]);

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!recipe) return null;

  return (
    <div className="bg-white p-4 sm:p-8 rounded-xl shadow-lg">
      <div className="flex justify-between items-start mb-6">
        <div><h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900">{recipe.title}</h1><p className="text-xl text-gray-600 mt-2">Yields: {recipe.yield_amount}</p></div>
        <button onClick={onBack} className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg">&larr; Back</button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1 bg-gray-50 p-6 rounded-lg"><h2 className="text-3xl font-bold mb-4 border-b-2 pb-2">Ingredients</h2><ul className="space-y-3 text-lg">{recipe.ingredients.map((ing, index) => (<li key={index} className="flex justify-between"><span>{ing.name}</span><span className="font-mono text-gray-700">{ing.quantity} {ing.unit}</span></li>))}</ul></div>
        <div className="md:col-span-2"><h2 className="text-3xl font-bold mb-4 border-b-2 pb-2">Instructions</h2><div className="prose prose-xl max-w-none text-gray-800 whitespace-pre-wrap">{recipe.instructions}</div></div>
      </div>
      <div className="mt-8 flex justify-end gap-4"><button onClick={() => onEdit(recipe)} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg">Edit</button></div>
    </div>
  );
};
