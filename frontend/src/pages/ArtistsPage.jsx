import React, { useEffect, useState } from 'react';
import './ArtistsPage.css';

export default function ArtistsPage() {
  const [artists, setArtists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [firstname, setFirstname] = useState('');
  const [lastname, setLastname] = useState('');

  // 🔐 Vérifie si l'utilisateur est admin (par username dans le token)
  let isAdmin = false;
try {
  const token = localStorage.getItem('access');
  if (token) {
    const payload = JSON.parse(atob(token.split('.')[1]));
    console.log('🧾 Payload JWT =', payload); // ← Regarde bien dans la console
    isAdmin = payload.username === 'admin';
  }
} catch (err) {
  console.error('Erreur JWT :', err);
}

  useEffect(() => {
    fetchArtists();
  }, []);

  const fetchArtists = async () => {
    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/artists/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      });

      if (!res.ok) throw new Error('Erreur lors du chargement des artistes');

      const data = await res.json();
      setArtists(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAddArtist = async (e) => {
    e.preventDefault();
    if (!firstname || !lastname) return;

    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/api/artists/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
        body: JSON.stringify({ firstname, lastname }),
      });

      if (!res.ok) throw new Error("Erreur lors de l'ajout de l'artiste");

      const newArtist = await res.json();
      setArtists([newArtist, ...artists]);
      setFirstname('');
      setLastname('');
      setShowForm(false);
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="artists-container">
      <h2 className="artists-title">🎭 Nos Artistes</h2>

      {/* ✅ Bouton visible uniquement pour admin */}
      {isAdmin && (
        <button className="add-button" onClick={() => setShowForm(!showForm)}>
          {showForm ? '❌ Annuler' : '➕ Ajouter un artiste'}
        </button>
      )}

      {/* ✅ Formulaire visible uniquement si showForm true */}
      {isAdmin && showForm && (
        <form onSubmit={handleAddArtist} className="artist-form">
          <input
            type="text"
            placeholder="Prénom"
            value={firstname}
            onChange={(e) => setFirstname(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Nom"
            value={lastname}
            onChange={(e) => setLastname(e.target.value)}
            required
          />
          <button type="submit">✅ Ajouter</button>
        </form>
      )}

      {loading ? (
        <p>Chargement...</p>
      ) : error ? (
        <p className="error">{error}</p>
      ) : (
        <div className="artist-grid">
          {artists.map((artist) => (
            <div className="artist-card" key={artist.id}>
              <div className="artist-name">
                {artist.firstname} {artist.lastname}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
