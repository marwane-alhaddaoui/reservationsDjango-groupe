import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './Navbar.css';

export default function Navbar() {
  const { isAuthenticated, logout } = useContext(AuthContext);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <h2>Projet Réservations</h2>
        <ul className="navbar-menu">
          <li><Link to="/" className="navbar-links">Accueil</Link></li>

          {isAuthenticated ? (
            <>
              <li><Link to="/profile" className="navbar-links">Profil</Link></li>
              <li>
                <button
                  onClick={logout}
                  className="navbar-links"
                  style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}
                >
                  Déconnexion
                </button>
              </li>
            </>
          ) : (
            <>
              <li><Link to="/login" className="navbar-links">Connexion</Link></li>
              <li><Link to="/register" className="navbar-links">Inscription</Link></li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
}
