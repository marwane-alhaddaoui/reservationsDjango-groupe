import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './Navbar.css'; // ou supprime cette ligne si tu utilises Tailwind

export default function Navbar() {
  const { isAuthenticated, logout } = useContext(AuthContext);
  console.log('Navbar – isAuthenticated =', isAuthenticated);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/', { replace: true });
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <h2>Projet Réservations</h2>
        <ul className="navbar-menu">
          {/* Lien Accueil toujours visible */}
          <li><Link to="/" className="navbar-links">Accueil</Link></li>

          {/* Si pas connecté : Connexion + Inscription */}
          {!isAuthenticated && (
            <>
              <li><Link to="/login" className="navbar-links">Connexion</Link></li>
              <li><Link to="/register" className="navbar-links">Inscription</Link></li>
            </>
          )}

          {/* Si connecté : Profil + Déconnexion */}
          {isAuthenticated && (
            <>
              <li><Link to="/profile" className="navbar-links">Profil</Link></li>
              <li>
                <button
                  onClick={handleLogout}
                  className="navbar-links"
                  style={{
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    padding: 0
                  }}
                >
                  Déconnexion
                </button>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
}
