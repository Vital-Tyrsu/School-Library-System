import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Login from './components/Login';
import Catalog from './components/Catalog';
import AdminDashboard from './components/AdminDashboard';

function App() {
  return (
    <Router>
      <div className="container">
        {/* Navigation Bar */}
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <Link className="navbar-brand" to="/">Library System</Link>
          <div className="navbar-nav">
            <Link className="nav-link" to="/login">Login</Link>
            <Link className="nav-link" to="/catalog">Catalog</Link>
            <Link className="nav-link" to="/admin">Admin</Link>
          </div>
        </nav>

        {/* Page Routes */}
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/catalog" element={<Catalog />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/" element={<Catalog />} /> {/* Default route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;