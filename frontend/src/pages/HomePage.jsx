import { useEffect, useState } from 'react';
import './HomePage.css';

const API_URL = process.env.REACT_APP_API_URL;

export default function HomePage() {
  const [shows, setShows] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const showsPerPage = 4;

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

  // 🔍 Filtrage dynamique
  const filteredShows = shows.filter((show) =>
    show.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // 🎯 Pagination logique
  const indexOfLastShow = currentPage * showsPerPage;
  const indexOfFirstShow = indexOfLastShow - showsPerPage;
  const currentShows = filteredShows.slice(indexOfFirstShow, indexOfLastShow);
  const totalPages = Math.ceil(filteredShows.length / showsPerPage);
  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div className="home-page">
      <section className="hero-section">
        <h1>Bienvenue sur le site de Réservations de Spectacles</h1>
        <p>Réservez vos places pour les spectacles de votre choix !</p>
      </section>

      <section className="upcoming-shows">
        <h2>Prochains spectacles</h2>

        {/* Barre de recherche */}
        <div className="search-bar">
          <input
            type="text"
            className="search-input"
            placeholder="🔍 Rechercher un spectacle..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setCurrentPage(1); // reset pagination à chaque recherche
            }}
          />
        </div>

        {/* Cartes des spectacles */}
        <div className="cards-container">
          {currentShows.length > 0 ? (
            currentShows.map((show) => (
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
                    {show.bookable ? 'Réserver' : 'Indisponible'}
                  </button>
                </div>
              </div>
            ))
          ) : (
            <p style={{ textAlign: 'center', marginTop: '2rem', color: '#888' }}>
              Aucun spectacle trouvé.
            </p>
          )}
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <>
            <div className="pagination">
              <button onClick={() => paginate(currentPage - 1)} disabled={currentPage === 1}>
                ◀
              </button>
              {[...Array(totalPages)].map((_, i) => (
                <button
                  key={i + 1}
                  onClick={() => paginate(i + 1)}
                  className={currentPage === i + 1 ? 'active' : ''}
                >
                  {i + 1}
                </button>
              ))}
              <button
                onClick={() => paginate(currentPage + 1)}
                disabled={currentPage === totalPages}
              >
                ▶
              </button>
            </div>

            <p style={{ textAlign: 'center', marginTop: '1rem', color: '#555' }}>
              Page {currentPage} sur {totalPages}
            </p>
          </>
        )}
      </section>
    </div>
  );
}
