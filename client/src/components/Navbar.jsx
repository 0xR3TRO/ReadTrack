import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/Navbar.css";

export default function Navbar() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <Link to="/">ReadTrack</Link>
            </div>
            {user && (
                <div className="navbar-links">
                    <Link to="/">Dashboard</Link>
                    <Link to="/books">Books</Link>
                    <Link to="/authors">Authors</Link>
                    <div className="navbar-user">
                        <span>{user.username}</span>
                        <button onClick={handleLogout} className="btn-logout">
                            Logout
                        </button>
                    </div>
                </div>
            )}
        </nav>
    );
}
