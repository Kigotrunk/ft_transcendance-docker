import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import "../css/menu.css";
import SportsEsportsIcon from "@mui/icons-material/SportsEsports";
import ChatIcon from "@mui/icons-material/Chat";
import LogoutIcon from "@mui/icons-material/Logout";
import { AuthContext } from "../AuthContext";

const Menu = () => {
  const { logout } = useContext(AuthContext);

  return (
    <>
      <div className="phone-menu">
        <div
          style={{ width: "100%", height: "80px", backgroundColor: "black" }}
        ></div>
        <Link to="/chat">
          <span>Game</span>
        </Link>
        <Link to="/chat">
          <span>Chat</span>
        </Link>
        <Link onClick={logout}>
          <span>Logout</span>
        </Link>
      </div>

      <div className="blured"></div>

      <div className="menu">
        <Link to="/chat">
          <SportsEsportsIcon fontSize="inherit"></SportsEsportsIcon>
        </Link>
        <Link to="/chat">
          <ChatIcon fontSize="inherit"></ChatIcon>
        </Link>

        <Link onClick={logout} style={{ marginTop: "auto" }}>
          <LogoutIcon fontSize="inherit"></LogoutIcon>
        </Link>
      </div>
    </>
  );
};

export default Menu;
