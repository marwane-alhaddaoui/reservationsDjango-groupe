import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(null);

  useEffect(() => {
    const storedAccess = localStorage.getItem('access');
    if (storedAccess) {
      setAccessToken(storedAccess);
    }
  }, []);

  const login = ({ access, refresh }) => {
    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);
    setAccessToken(access);
  };

  const logout = () => {
    setAccessToken(null);
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
  };

  const isAuthenticated = !!accessToken;

  return (
    <AuthContext.Provider value={{ accessToken, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
}
