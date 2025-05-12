import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

function HomePage() {
  const [spectacles, setSpectacles] = useState([]);

  useEffect(() => {
    axios.get("/api/catalogue/shows/")
      .then(response => {
        setSpectacles(response.data.slice(0, 3));
      })
      .catch(error => {
        console.error("Erreur lors de la récupération des spectacles :", error);
      });
  }, []);

  return (
    <div className="text-center">
      <h1 className="mb-4">Bienvenue sur notre plateforme de réservation</h1>
      <p className="lead">Réservez vos places en ligne pour les meilleurs spectacles.</p>

      <div className="my-4">
        <Link to="/shows" className="btn btn-primary me-2">Voir le catalogue</Link>
      </div>

      <hr className="my-5" />

      <h2>Spectacles à venir</h2>
      <div className="row justify-content-center">
        {spectacles.map(s => (
          <div key={s.id} className="col-md-3 m-2 p-3 border rounded bg-white shadow-sm">
            <h5>{s.title}</h5>
            <p><strong>Date :</strong> {s.created_at}</p>
            <p><strong>Prix :</strong> {s.price ? s.price + "€" : "Non précisé"}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default HomePage;
