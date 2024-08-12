import React, { useContext, useEffect, useState } from "react";
import "../css/header.css";
import SearchIcon from "@mui/icons-material/Search";
import MenuIcon from "@mui/icons-material/Menu";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../AuthContext";
import { useTranslation } from "react-i18next";

const Header = ({ setShowPhoneMenu }) => {
    const { t } = useTranslation();
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);
  const [research, setResearch] = useState("");

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (research === "") {
      return;
    }
    navigate(`/search/${research}`);
  };

  return (
    <div className="header">
      <div className="btn-menu" onClick={() => setShowPhoneMenu(true)}>
        <MenuIcon></MenuIcon>
      </div>
      <Link to="/home" className="logo">
        <h3>PONG</h3>
      </Link>
      <form className="search-bar" onSubmit={handleSearchSubmit}>
        <input
          type="text"
          placeholder={t('Search')}
          onChange={(e) => setResearch(e.target.value)}
        />
        <button type="submit">
          <SearchIcon></SearchIcon>
        </button>
      </form>
      <Link to={`profile/${user.id}`} className="user">
        <span>
          <img
            src={`https://localhost:8000${user.profile_picture}`}
            alt="profile picture"
          />
        </span>
        <span className="username">{user.username}</span>
      </Link>
    </div>
  );
};

export default Header;
