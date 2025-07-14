export const api = {
  baseUrl: process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000',
    get: async <T,>(url: string, token: string): Promise<T> => {
      const response = await fetch(`${api.baseUrl}${url}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    },
    post: async <T,>(url: string, data: any, token?: string | null): Promise<T> => {
      const response = await fetch(`${api.baseUrl}${url}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token && {'Authorization': `Bearer ${token}`}),
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Network response was not ok');
      }
      return response.json();
    },
    put: async <T,>(url: string, data: any, token: string): Promise<T> => {
      const response = await fetch(`${api.baseUrl}${url}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    },
    delete: async (url: string, token: string): Promise<boolean> => {
      const response = await fetch(`${api.baseUrl}${url}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.status !== 204) throw new Error('Network response was not ok');
      return true;
    },
  };