import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function ArtistDetail() {
  const { id } = useParams();
  const [artist, setArtist] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    axios.get(`/api/catalogue/artists/${id}/`)
      .then(response => setArtist(response.data))
      .catch(() => setError("Impossible de charger l'artiste."));
  }, [id]);

  if (error) return <p className="text-danger">{error}</p>;
  if (!artist) return <p>Chargement...</p>;

  return (
    <div className="container mt-4">
      <h2>Détail de l'artiste</h2>
      <div className="card mt-3">
        <div className="card-body">
          <h4 className="card-title">{artist.firstname} {artist.lastname}</h4>
        </div>
      </div>
    </div>
  );
}

export default ArtistDetail;
