import React from 'react';
import { useHistory } from 'react-router-dom';
import './menu.css';

const Menu = () => {
  const history = useHistory();

  const gameSection = () => {
    // Implement gameSection logic
  };

  const showChatList = () => {
    history.push('/chat');
  };

  return (
    <>
      <div className="phone-menu">
        <div style={{ width: '100%', height: '80px', backgroundColor: 'black' }}></div>
        <a onClick={gameSection}><span>Game</span></a>
        <a onClick={showChatList}><span>Chat</span></a>
        <a href="/settings"><span>Settings</span></a>
      </div>

      <div className="blured"></div>

        <div className="menu short-menu">
          <a onClick={gameSection}><span className="material-icons">sports_esports</span></a>
          <a onClick={showChatList}><span className="material-icons">chat</span></a>
          <a href="/logout" style={{ marginTop: 'auto' }}><span className="material-icons">logout</span></a>
        </div>

        <div className="menu extanded-menu">
          <a onClick={gameSection}><span className="material-icons">sports_esports</span><span>Game</span></a>
          <a onClick={showChatList}><span className="material-icons">chat</span><span>Chat</span></a>
          <a href="/logout" style={{ marginTop: 'auto' }}><span className="material-icons">logout</span><span>Logout</span></a>
        </div>
    </>
  );
};

export default Menu;
