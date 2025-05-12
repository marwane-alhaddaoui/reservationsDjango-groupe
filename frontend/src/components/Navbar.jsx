import { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";

function Navbar() {
  const { isLoggedIn, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container">
        <Link className="navbar-brand" to="/">Réservations</Link>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/shows">Spectacles</Link>
            </li>
          </ul>
          <ul className="navbar-nav ms-auto">
            {!isLoggedIn ? (
              <li className="nav-item">
                <Link className="nav-link" to="/login">Se connecter</Link>
              </li>
            ) : (
              <li className="nav-item">
                 <Link className="nav-link" to="/profile">Mon profil</Link>
                <button className="btn btn-link nav-link" onClick={handleLogout}>
                  Se déconnecter
                </button>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
