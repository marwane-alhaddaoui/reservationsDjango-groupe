import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import { AuthProvider } from "./contexts/AuthContext";
import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import ShowList from "./pages/ShowList";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import PrivateRoute from "./components/PrivateRoute";
import ArtistList from "./pages/ArtistList";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <div className="container mt-4">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/shows" element={<ShowList />} />
            <Route path="/login" element={<Login />} />
            <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
            <Route path="/artists" element={<ArtistList />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
