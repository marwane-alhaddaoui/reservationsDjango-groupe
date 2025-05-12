import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage"; 
import ShowList from "./pages/ShowList";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <Router>
      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/shows" element={<ShowList />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
