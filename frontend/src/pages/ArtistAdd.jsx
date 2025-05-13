import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function ArtistAdd() {
  const [firstname, setFirstname] = useState("");
  const [lastname, setLastname] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    const token = localStorage.getItem("access");
    if (!token) {
      setError("Vous devez être connecté pour ajouter un artiste.");
      return;
    }

    axios.post("/api/catalogue/artists/", {
      firstname,
      lastname
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(() => {
      navigate("/artists");
    })
    .catch(() => {
      setError("Une erreur est survenue lors de l'ajout.");
    });
  };

  return (
    <div className="container mt-5" style={{ maxWidth: "500px" }}>
      <h2 className="mb-4 text-center">Ajouter un artiste</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="firstname" className="form-label">Prénom</label>
          <input
            type="text"
            className="form-control"
            id="firstname"
            value={firstname}
            onChange={(e) => setFirstname(e.target.value)}
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="lastname" className="form-label">Nom</label>
          <input
            type="text"
            className="form-control"
            id="lastname"
            value={lastname}
            onChange={(e) => setLastname(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary w-100">Ajouter</button>
      </form>
    </div>
  );
}

export default ArtistAdd;
