import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { useContext } from "react";
import { AuthContext } from "../contexts/AuthContext";

function ArtistList() {
  const [artists, setArtists] = useState([]);
  const { isLoggedIn } = useContext(AuthContext);

  useEffect(() => {
    axios.get("/api/catalogue/artists/")
      .then(response => setArtists(response.data))
      .catch(error => console.error("Erreur :", error));
  }, []);

  return (
  <div className="container mt-4">
    <h2 className="mb-4 text-center">Liste des artistes</h2>

    {isLoggedIn && (
      <div className="text-end mb-3">
        <Link to="/artist/add" className="btn btn-success">
          Ajouter un artiste
        </Link>
      </div>
    )}

    <div className="row">
      {artists.map(artist => (
        <div key={artist.id} className="col-md-4 mb-4">
          <div className="card shadow-sm h-100">
            <div className="card-body">
              <h5 className="card-title">{artist.firstname} {artist.lastname}</h5>
              <Link to={`/artists/${artist.id}`} className="btn btn-outline-primary btn-sm">
                Voir le détail
              </Link>
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>
);

}

export default ArtistList;
