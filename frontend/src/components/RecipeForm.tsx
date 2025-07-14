import React, { useState, FC } from 'react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../services/api';
import { Recipe, Ingredient } from '../types';

interface RecipeFormProps {
  recipe: Recipe | null;
  onSave: () => void;
  onCancel: () => void;
}

export const RecipeForm: FC<RecipeFormProps> = ({ recipe, onSave, onCancel }) => {
  const [title, setTitle] = useState(recipe?.title || '');
  const [instructions, setInstructions] = useState(recipe?.instructions || '');
  const [yieldAmount, setYieldAmount] = useState(recipe?.yield_amount || '');
  const [ingredients, setIngredients] = useState<Ingredient[]>(recipe?.ingredients || [{ name: '', quantity: '', unit: '' }]);
  const { token } = useAuth();

  const handleIngredientChange = (index: number, field: keyof Ingredient, value: string) => {
    const newIngredients = [...ingredients];
    newIngredients[index] = { ...newIngredients[index], [field]: value };
    setIngredients(newIngredients);
  };

  const addIngredient = () => setIngredients([...ingredients, { name: '', quantity: '', unit: '' }]);
  const removeIngredient = (index: number) => setIngredients(ingredients.filter((_, i) => i !== index));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) return;
    const recipeData = { title, instructions, yield_amount: yieldAmount, ingredients };
    try {
      if (recipe?.id) {
        await api.put(`/api/recipes/${recipe.id}/`, recipeData, token);
      } else {
        await api.post('/api/recipes/', recipeData, token);
      }
      onSave();
    } catch (error) {
      console.error("Failed to save recipe", error);
      alert("Failed to save recipe. Check console for details.");
    }
  };

  return (
    <div className="bg-white p-8 rounded-xl shadow-lg">
        <h2 className="text-3xl font-bold mb-6">{recipe?.id ? 'Edit Recipe' : 'Create New Recipe'}</h2>
        <form onSubmit={handleSubmit}>
            <div className="mb-4"><label className="block text-gray-700 font-bold mb-2">Title</label><input type="text" value={title} onChange={e => setTitle(e.target.value)} className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" required /></div>
            <div className="mb-4"><label className="block text-gray-700 font-bold mb-2">Yield</label><input type="text" value={yieldAmount} onChange={e => setYieldAmount(e.target.value)} className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g., 4 servings" required /></div>
            <div className="mb-6"><label className="block text-gray-700 font-bold mb-2">Instructions</label><textarea value={instructions} onChange={e => setInstructions(e.target.value)} className="w-full p-3 border rounded-lg h-40 focus:outline-none focus:ring-2 focus:ring-blue-500" required /></div>
            <h3 className="text-2xl font-bold mb-4">Ingredients</h3>
            {ingredients.map((ing, index) => (
                <div key={index} className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4 items-center">
                    <input type="text" value={ing.name} onChange={e => handleIngredientChange(index, 'name', e.target.value)} className="md:col-span-2 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Ingredient Name" required />
                    <input type="number" step="any" value={ing.quantity} onChange={e => handleIngredientChange(index, 'quantity', e.target.value)} className="p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Qty" required />
                    <div className="flex items-center"><input type="text" value={ing.unit} onChange={e => handleIngredientChange(index, 'unit', e.target.value)} className="p-3 border rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Unit" required /><button type="button" onClick={() => removeIngredient(index)} className="ml-2 text-red-500 hover:text-red-700 font-bold text-2xl">&times;</button></div>
                </div>
            ))}
            <button type="button" onClick={addIngredient} className="mb-6 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg">+ Add Ingredient</button>
            <div className="flex justify-end gap-4"><button type="button" onClick={onCancel} className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-6 rounded-lg">Cancel</button><button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg">Save Recipe</button></div>
        </form>
    </div>
  );
};