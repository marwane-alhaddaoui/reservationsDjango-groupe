import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './HomePage.css';

const API_URL = process.env.REACT_APP_API_URL;

export default function HomePage() {
  const { isAuthenticated, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [shows, setShows] = useState([]);

  useEffect(() => {
    const fetchShows = async () => {
      try {
        const response = await fetch(`${API_URL}/api/shows/`);
        const data = await response.json();
        setShows(data);
      } catch (error) {
        console.error('Erreur lors du chargement des spectacles :', error);
      }
    };

    fetchShows();
  }, []);

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

      {/* Prochains spectacles */}
      <section className="upcoming-shows">
        <h2>Prochains spectacles</h2>
        <div className="cards-container">
          {shows.map((show) => (
            <div key={show.id} className="show-card">
              <img
                src={`https://picsum.photos/seed/${encodeURIComponent(show.title)}/300/200`}
                alt={show.title}
                className="show-image"
              />
              <div className="show-info">
                <h3>{show.title}</h3>
                <p className="description">{show.description}</p>
                <p className="price">Prix : {parseFloat(show.price).toFixed(2)} €</p>
                <button className="reserve-button" disabled={!show.bookable}>
                  {show.bookable ? "Réserver" : "Indisponible"}
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
