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
import Login from './components/Login';
import Logout from './components/Logout';
import Profile from './components/Profile';
import PageNotFound from './utils/PageNotFound';
// import Register from './components/Register';
// import AuthProvider from './AuthProvider';


const App = () => {

  const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken'));

  return (
    <Router>
      {accessToken ? (
        <>
          <Header/>
          <div style={{ display: 'flex', flexDirection: 'row', flexGrow: 1 }}>
            <Menu/>
            <div className="content" style={{ flexGrow: 1 }}>
              <Routes>
                <Route exact path="/" element={<Home />} />
                <Route path="/pong" element={<Pong />} />
                <Route path="/chat" element={<Chat />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/logout" element={<Logout setAccessToken={setAccessToken} />} />
                <Route path="*" element={<PageNotFound />} />
              </Routes>
            </div>
          </div>
        </>
      ) : (
        <Routes>
          <Route exact path="/" element={<Login setAccessToken={setAccessToken} />} />
          <Route exact path="/login" element={<Login setAccessToken={setAccessToken} />} />
          {/* <Route path="/register" element={<Register />} /> */}
        </Routes>
      )}
    </Router>
  );
};

export default App;