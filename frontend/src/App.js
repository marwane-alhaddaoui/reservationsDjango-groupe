import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import { AuthContext } from './context/AuthContext';
import './index.css';

export default function App() {
  const { isAuthenticated } = useContext(AuthContext);

  return (
    <Router>
      <Navbar />
      <div style={{ marginLeft: '200px', padding: '20px' }}>
        <Routes>
          <Route path="/" element={<HomePage />} />

          {/* si non connecté, afficher LoginPage ; sinon rediriger vers /profile */}
          <Route
            path="/login"
            element={
              !isAuthenticated ? <LoginPage /> : <Navigate to="/" replace />
            }
          />

          {/* idem pour register */}
          <Route
            path="/register"
            element={
              !isAuthenticated ? <RegisterPage /> : <Navigate to="/" replace />
            }
          />
          <Route path="/profile" element={isAuthenticated ? <ProfilePage /> : <Navigate to="/login" replace />}/>
        </Routes>
      </div>
    </Router>
  );
}
