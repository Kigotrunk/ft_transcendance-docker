import React, { useState, useEffect } from 'react';
import '../css/menu.css';
import { useNavigate } from "react-router-dom";
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';
import ChatIcon from '@mui/icons-material/Chat';
import LogoutIcon from '@mui/icons-material/Logout';

const Menu = () => {

	const navigate = useNavigate();

  

  return (
    <>
      <div className="phone-menu">
        <div style={{ width: '100%', height: '80px', backgroundColor: 'black' }}></div>
        <a onClick={() => navigate("/chat")}><span>Game</span></a>
        <a onClick={() => navigate("/chat")}><span>Chat</span></a>
        <a href="/settings"><span>Settings</span></a>
      </div>

      <div className="blured"></div>

        <div className="menu short-menu">
          <a onClick={() => navigate("/chat")}><SportsEsportsIcon></SportsEsportsIcon></a>
          <a onClick={() => navigate("/chat")}><ChatIcon></ChatIcon></a>
          <a href="/logout" style={{ marginTop: 'auto' }}><LogoutIcon></LogoutIcon></a>
        </div>

        <div className="menu extanded-menu">
          <a onClick={() => navigate("/chat")}><SportsEsportsIcon></SportsEsportsIcon><span>Game</span></a>
          <a onClick={() => navigate("/chat")}><ChatIcon></ChatIcon><span>Chat</span></a>
          <a href="/logout" style={{ marginTop: 'auto' }}><LogoutIcon></LogoutIcon><span>Logout</span></a>
        </div>
    </>
  );
};

export default Menu;
