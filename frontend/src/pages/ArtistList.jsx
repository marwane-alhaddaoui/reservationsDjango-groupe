import { useEffect, useState } from "react";
import axios from "axios";

function ArtistList() {
  const [artists, setArtists] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("/api/catalogue/artists/")
      .then(response => {
        setArtists(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Erreur lors de la récupération des artistes :", error);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Chargement des artistes...</p>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4 text-center">Liste des artistes</h2>
      <div className="row">
        {artists.map(artist => (
          <div key={artist.id} className="col-md-4 mb-4">
            <div className="card shadow-sm h-100">
              <div className="card-body">
                <h5 className="card-title">{artist.firstname} {artist.lastname}</h5>
                <a href={artist.links.self} className="btn btn-outline-primary btn-sm" target="_blank" rel="noreferrer">
                  Voir le détail
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ArtistList;
