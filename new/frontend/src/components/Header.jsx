import React from 'react';
import '../css/header.css';
import SearchIcon from '@mui/icons-material/Search';
import MenuIcon from '@mui/icons-material/Menu';
import { Link } from 'react-router-dom';

const Header = () => {
  
  const showMenu = () => {
    // Implement showMenu logic
  };

  return (
    <div className="header">
      <a className="btn-menu" onClick={showMenu}><MenuIcon></MenuIcon></a>
      <Link to="/" className="logo"><h3>PONG</h3></Link>
      <div className="search-bar">
        <input type="text" placeholder="Search" />
        <button><SearchIcon></SearchIcon></button>
      </div>
      <Link to="/profile" className="user">
        <span>
          <img id="id_profile_links" data-toggle="dropdown" aria-haspopup="true"
            aria-expanded="false" src=""/* Add your profile picture URL here */ alt="profile logo" width="40" height="40" />
        </span>
        <span className="username">{/* Add username here */}</span>
      </Link>
    </div>
  );
};

export default Header;
