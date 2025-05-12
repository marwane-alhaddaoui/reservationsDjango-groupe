import { useEffect, useState } from "react";
import axios from "axios";

function ShowList() {
  const [shows, setShows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("/api/catalogue/shows/")
      .then(response => {
        setShows(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Erreur lors de la récupération des spectacles :", error);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Chargement des spectacles...</p>;

  return (
    <div className="container">
      <h2 className="mb-4 text-center">Liste des spectacles</h2>
      <div className="row">
        {shows.map((show) => (
          <div key={show.id} className="col-md-4 mb-4">
            <div className="card h-100 shadow-sm">
              <div className="card-body">
                <h5 className="card-title">{show.title || "Titre non spécifié"}</h5>
                <p className="card-text"><strong>Date :</strong> {show.date || "Inconnue"}</p>
                <p className="card-text"><strong>Prix :</strong> {show.price ? show.price + "€" : "Non spécifié"}</p>
                <p className="card-text"><strong>Lieu :</strong> {show.place || "Inconnu"}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ShowList;
