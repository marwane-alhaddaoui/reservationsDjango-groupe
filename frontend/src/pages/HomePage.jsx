import React from 'react';
import './HomePage.css';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="main-content">
      <div className="top-bar">
        <input
          type="text"
          placeholder="Rechercher un spectacle..."
          className="search-bar"
        />
       <div className="auth-buttons">
  <Link to="/login" className="btn-login">Se connecter</Link>
  <Link to="/register" className="btn-signup">S'inscrire</Link>
</div>
      </div>

      <section className="hero-section">
        <h1>Bienvenue 🎟️</h1>
        <p>Réservez vos places pour les meilleurs spectacles !</p>
      </section>

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
              <td>À voir et à revoir</td>
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
};

export default HomePage;
