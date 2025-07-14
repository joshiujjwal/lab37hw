import React, { useState, createContext, FC, ReactNode } from 'react';
import { api } from '../services/api';
import { AuthContextType } from '../types';

export const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: FC<{children: ReactNode}> = ({ children }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('authToken'));

  const login = async (username: string, password: string) => {
    try {
      const data = await api.post<{access: string}>('/api/token/', { username, password });
      localStorage.setItem('authToken', data.access);
      setToken(data.access);
    } catch (error) {
      console.error("Login failed:", error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
  };

  const value = { token, login, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};