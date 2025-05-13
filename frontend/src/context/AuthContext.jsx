import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(
    () => localStorage.getItem('access') || null
  );

  // À chaque changement de token, on met à jour le localStorage
  useEffect(() => {
    if (accessToken) {
      localStorage.setItem('access', accessToken);
    } else {
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
    }
  }, [accessToken]);

  const login = ({ access, refresh }) => {
    setAccessToken(access);
    localStorage.setItem('refresh', refresh);
  };

  const logout = () => {
    setAccessToken(null);
  };

  const isAuthenticated = Boolean(accessToken);

  return (
    <AuthContext.Provider value={{ accessToken, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
}