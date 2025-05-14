import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './HomePage.css';

export default function HomePage() {
  const { isAuthenticated, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/', { replace: true });
  };

  return (
    <div className="home-page">
      {/* Hero */}
      <section className="hero-section">
        <h1>Bienvenue sur le site de Réservations de Spectacles</h1>
        <p>Réservez vos places pour les spectacles de votre choix !</p>
      </section>

      {/* Actions utilisateur */}
      <section className="auth-actions">
        {!isAuthenticated ? (
          <>
            <Link to="/login" className="btn-auth">
              Se connecter
            </Link>
            <Link to="/register" className="btn-auth">
              S'inscrire
            </Link>
          </>
        ) : (
          <button onClick={handleLogout} className="btn-auth">
            Se déconnecter
          </button>
        )}
      </section>

      {/* Prochains spectacles */}
      <section className="upcoming-shows">
        <h2>Prochains spectacles</h2>
        <table className="shows-table">
          <thead>
            <tr>
              <th>Titre</th>
              <th>Auteur</th>
              <th>Lieu</th>
              <th>Prix</th>
              <th>Réservable</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Le spectacle de la vie</td>
              <td>John Doe</td>
              <td>Palais des Arts</td>
              <td>9,50 €</td>
              <td>Oui</td>
            </tr>
            <tr>
              <td>Du haut de mon perchoir</td>
              <td>Smith Durand</td>
              <td>Grand Palace</td>
              <td>15,00 €</td>
              <td>Non</td>
            </tr>
            <tr>
              <td>A voir et à revoir</td>
              <td>Bob Sull</td>
              <td>Palais des Arts</td>
              <td>10,50 €</td>
              <td>Oui</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  );
}
