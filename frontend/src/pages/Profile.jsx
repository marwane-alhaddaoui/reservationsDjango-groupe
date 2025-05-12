import { useEffect, useState } from "react";
import axios from "axios";

function Profile() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access");

    axios.get("/api/catalogue/user/", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(response => {
      setUser(response.data);
    })
    .catch(() => {
      setError("Impossible de charger les informations utilisateur.");
    });
  }, []);

  if (error) return <p className="text-danger">{error}</p>;
  if (!user) return <p>Chargement...</p>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Mon profil</h2>
      <ul className="list-group">
        <li className="list-group-item"><strong>Nom d'utilisateur :</strong> {user.username}</li>
        <li className="list-group-item"><strong>Email :</strong> {user.email}</li>
        <li className="list-group-item"><strong>Admin :</strong> {user.is_staff ? "Oui" : "Non"}</li>
      </ul>
    </div>
  );
}

export default Profile;
