import { Link } from "react-router-dom";
import { useEffect, useState } from "react";

function HomePage() {
  const [spectacles, setSpectacles] = useState([]);

  useEffect(() => {
    // Simulation de spectacles à venir
    setSpectacles([
      { id: 1, title: "Spectacle 1", date: "2024-06-01", lieu: "Bruxelles" },
      { id: 2, title: "Spectacle 2", date: "2024-06-10", lieu: "Liège" },
      { id: 3, title: "Spectacle 3", date: "2024-06-15", lieu: "Namur" }
    ]);
  }, []);

  return (
    <div className="text-center">
      <h1 className="mb-4">Bienvenue sur notre plateforme de réservation</h1>
      <p className="lead">
        Découvrez les meilleurs spectacles et réservez vos places en ligne !
      </p>

      <div className="my-4">
        <Link to="/shows" className="btn btn-primary me-2">Voir le catalogue</Link>
        <Link to="/login" className="btn btn-outline-secondary">Se connecter</Link>
      </div>

      <hr className="my-5" />

      <h2>Spectacles à venir</h2>
      <div className="row justify-content-center">
        {spectacles.map(s => (
          <div key={s.id} className="col-md-3 m-2 p-3 border rounded bg-white shadow-sm">
            <h5>{s.title}</h5>
            <p><strong>Date :</strong> {s.date}</p>
            <p><strong>Lieu :</strong> {s.lieu}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default HomePage;
