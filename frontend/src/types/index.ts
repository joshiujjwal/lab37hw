export interface Ingredient {
    name: string;
    quantity: number | string;
    unit: string;
  }
  
  export interface Recipe {
    id: number;
    title: string;
    instructions: string;
    yield_amount: string;
    ingredients: Ingredient[];
    updated_at: string;
  }
  
  export interface RecipeSummary {
      id: number;
      title: string;
      yield_amount: string;
  }
  
  export interface AuthContextType {
    token: string | null;
    login: (username: string, password: string) => Promise<void>;
    logout: () => void;
  }