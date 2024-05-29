import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import './css/colors.css';
import './css/index.css';
import Header from './components/Header';
import Menu from './components/Menu';
import Home from './components/Home';
import Chat from './components/Chat';
import Pong from './components/Pong';
// import Accueil from './components/Accueil';
// import Login from './components/Login';
// import Register from './components/Register';


const App = () => {
  const [isLog, setLog] = useState(false);
  return (
    <Router>
      {/* isLog ? ( */}
        <>
          <Header />
          <div style={{ display: 'flex', flexDirection: 'row', flexGrow: 1 }}>
            <Menu />
            <div className="content" style={{ flexGrow: 1 }}>
              <Routes>
                <Route exact path="/" element={<Home />} />
                <Route path="/pong" element={<Pong />} />
                <Route path="/chat" element={<Chat />} />
              </Routes>
            </div>
          </div>
        </>
      {/* ) : (
      <Routes>
        <Route exact path="/" element={<Accueil />} />
          <Route exact path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      ) */}
    </Router>
  );
};

export default App;