import React, { useEffect, useContext, useState } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import "../css/menu.css";
import SportsEsportsIcon from "@mui/icons-material/SportsEsports";
import ChatIcon from "@mui/icons-material/Chat";
import TimelineIcon from "@mui/icons-material/Timeline";
import LogoutIcon from "@mui/icons-material/Logout";
import { AuthContext } from "../AuthContext";
import Notif from "./Notif";
import { useTranslation } from "react-i18next";

const Menu = ({ showPhoneMenu, setShowPhoneMenu }) => {
    const { t } = useTranslation();
  const { logout, user, chatSocketRef, chatNotifsId, setChatNotifsId } =
    useContext(AuthContext);
  const [gameNotifs, setGameNotifs] = useState(false);
  const navigate = useNavigate();
  // const [notifs, setNotifs] = useState([]);

  const addChatNotif = (e) => {
    const data = JSON.parse(e.data);
    if (data.issuer === user.username) return;
    console.log(data);
    if (data.issuer === "Tournament Info") {
      if (window.location.pathname !== "/game") setGameNotifs(true);
      return;
    }
    setChatNotifsId((prev) => {
      if (prev.includes(data.conversation_id)) return prev;
      return [...prev, data.conversation_id];
    });
    // setNotifs((prev) => {
    //   return [...prev, { issuer: data.issuer, message: data.message }];
    // });
  };

  useEffect(() => {
    if (!chatSocketRef.current) {
      console.log("menu: No chat socket");
      return;
    }
    console.log("menu: Adding chat notif listener");
    chatSocketRef.current.addEventListener("message", addChatNotif);
    return () => {
      if (chatSocketRef.current) {
        chatSocketRef.current.removeEventListener("message", addChatNotif);
      }
    };
  }, [chatSocketRef.current]);

  return (
    <>
      {/* {notifs.length > 0 && <Notif notifs={notifs} />} */}
      {showPhoneMenu && (
        <>
          <div className="phone-menu">
            <div
              style={{
                width: "100%",
                height: "80px",
                backgroundColor: "black",
                fontSize: "2rem",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                fontWeight: "bold",
              }}
              onClick={() => navigate("/")}
            >
              PONG
            </div>
            <NavLink
              to="/game"
              onClick={() => {
                setGameNotifs(false);
                setShowPhoneMenu(false);
              }}
            >
              <span>{t('Game')}</span>
            </NavLink>
            <NavLink to="/chat" onClick={() => setShowPhoneMenu(false)}>
              <span>Chat</span>
            </NavLink>
            <Link onClick={logout}>
              <span>{t('Logout')}</span>
            </Link>
          </div>

          <div className="blured" onClick={() => setShowPhoneMenu(false)}></div>
        </>
      )}

      <div className="menu">
        <NavLink to="/game" onClick={() => setGameNotifs(false)}>
          <SportsEsportsIcon fontSize="inherit"></SportsEsportsIcon>
          {gameNotifs && <div className="notif">!</div>}
        </NavLink>

        <NavLink to="/chat">
          <ChatIcon fontSize="inherit"></ChatIcon>
          {chatNotifsId.length > 0 && (
            <div className="notif">{chatNotifsId.length}</div>
          )}
        </NavLink>

        <NavLink to={`/stats/${user.id}`}>
          <TimelineIcon fontSize="inherit"></TimelineIcon>
        </NavLink>

        <Link onClick={logout} style={{ marginTop: "auto" }}>
          <LogoutIcon fontSize="inherit"></LogoutIcon>
        </Link>
      </div>
    </>
  );
};

export default Menu;
