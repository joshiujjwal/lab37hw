import React, { useState, FC } from 'react';
import { useAuth } from './hooks/useAuth';
import { Login } from './components/Login';
import { Dashboard } from './components/Dashboard';
import { RecipeDetail } from './components/RecipeDetail';
import { RecipeForm } from './components/RecipeForm';
import { Recipe } from './types';

type View = 'dashboard' | 'detail' | 'form';

const App: FC = () => {
  const { token } = useAuth();
  const [view, setView] = useState<View>('dashboard');
  const [selectedRecipeId, setSelectedRecipeId] = useState<number | null>(null);
  const [recipeToEdit, setRecipeToEdit] = useState<Recipe | null>(null);

  if (!token) {
    return <Login />;
  }
  
  const handleSave = () => {
      setView('dashboard');
      setSelectedRecipeId(null);
      setRecipeToEdit(null);
  }
  
  const handleSetView = (newView: View) => {
      if (newView === 'form') {
          setRecipeToEdit(null); // Clear previous recipe if creating a new one
      }
      setView(newView);
  }

  return (
    <div className="bg-gray-100 min-h-screen p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        {view === 'dashboard' && <Dashboard setView={handleSetView} setSelectedRecipeId={setSelectedRecipeId} setRecipeToEdit={setRecipeToEdit} />}
        {view === 'detail' && selectedRecipeId && <RecipeDetail recipeId={selectedRecipeId} onBack={() => setView('dashboard')} onEdit={(recipe) => { setRecipeToEdit(recipe); setView('form'); }} />}
        {view === 'form' && <RecipeForm recipe={recipeToEdit} onSave={handleSave} onCancel={() => setView('dashboard')} />}
      </div>
    </div>
  );
}

export default App;