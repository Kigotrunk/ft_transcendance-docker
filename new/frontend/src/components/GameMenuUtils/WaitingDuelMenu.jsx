import React, { useContext, useState, useEffect } from "react";
import { AuthContext } from "../../AuthContext";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import axios from "axios";
import { useTranslation } from "react-i18next";

const WaitingDuelMenu = ({ setMenuState, queueState }) => {
  const [inQueue, setInQueue] = useState(queueState);
  const { t } = useTranslation();
  const leaveQueue = async () => {
    try {
      const response = await axios.post(
        "https://localhost:8000/game/leave_queue/"
      );
      console.log(response.data);
      setInQueue(false);
    } catch (error) {
      console.error(error);
    }
  };

  const joinQueue = async () => {
    try {
      const response = await axios.post(
        "https://localhost:8000/game/join_queue/"
      );
      console.log(response.data);
      setInQueue(true);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="cup-menu">
      <h2>{('Duel')}</h2>
      {inQueue ? (
        <div className="menu-queue-state">
          <span>{t('Waiting for opponent...')}</span>
          <div className="loader"></div>
          <div className="cancel-btn" onClick={leaveQueue}>
            {t('Cancel')}
          </div>
        </div>
      ) : (
        <div className="join-btn" onClick={joinQueue}>
          {t('Find a game')}
        </div>
      )}
      <button
        className="btn-back"
        onClick={() => {
          setMenuState("main");
          leaveQueue();
        }}
      >
        <ArrowBackIcon fontSize="large" />
      </button>
    </div>
  );
};

export default WaitingDuelMenu;
