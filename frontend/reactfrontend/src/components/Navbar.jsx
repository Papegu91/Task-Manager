import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthProvider';
import './Navbar.css'; // Import the CSS file if needed

const Navbar = () => {
    const { logout } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login'); // Redirect to login page after logout
    };

    return (
        <nav className="navbar">
            <ul>
                <li>
                    <Link to="/tasks">Task List</Link>
                </li>
                <li>
                    <Link to="/tasks/new" className="navbar-button">Create Task</Link>
                </li>
                <li>
                    <Link to="/tags/new" className="navbar-button">Create Tag</Link>
                </li>
                <li>
                    <Link to="/tags" className="navbar-button">Tag List</Link>
                </li>
                <li>
                    <button onClick={handleLogout} className="navbar-button">Logout</button>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
