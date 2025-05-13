import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <h2>🎭 Réservations</h2>
        <ul className="navbar-menu">
          <li><Link to="/" className="navbar-links">Accueil</Link></li>
          <li><Link to="/upcoming-shows" className="navbar-links">Spectacles</Link></li>
          <li><Link to="/profile" className="navbar-links">Profil</Link></li>
          <li><Link to="/reservations" className="navbar-links">Mes réservations</Link></li>
          <li><Link to="/admin" className="navbar-links">Admin</Link></li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
