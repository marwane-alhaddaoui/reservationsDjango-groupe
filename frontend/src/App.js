import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';  // Importer la page d'accueil
import Navbar from './components/Navbar';  // Importer la barre de navigation

const App = () => {
  return (
    <Router>
      <Navbar />
      <div style={{ marginLeft: '200px', padding: '20px' }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          {/* Ajoute ici d'autres routes si nécessaire */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;
