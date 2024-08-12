import React, { useState, useContext, useEffect } from "react";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import axios from "axios";
import { useTranslation } from "react-i18next";

const TournamentMenu = ({ setMenuState, queueState }) => {
  const [inQueue, setInQueue] = useState(queueState);
  const { t } = useTranslation();
  const leaveCup = async () => {
    try {
      const response = await axios.post(
        "https://localhost:8000/game/leave_cup/"
      );
      console.log(response.data);
      setInQueue(false);
    } catch (error) {
      console.error(error);
    }
  };

  const joinCup = async () => {
    try {
      const response = await axios.post("https://localhost:8000/game/join_cup/");
      console.log(response.data);
      setInQueue(true);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="cup-menu">
      <h2>{t('Tournament')}</h2>
      {inQueue ? (
        <div className="menu-queue-state">
          <span>{t('Waiting for more players...')}</span>
          <div className="loader"></div>
          <div className="cancel-btn" onClick={leaveCup}>
            {t('Cancel')}
          </div>
        </div>
      ) : (
        <div className="join-btn" onClick={joinCup}>
          {t('Join')}
        </div>
      )}
      <button
        className="btn-back"
        onClick={() => {
          setMenuState("main");
          leaveCup();
        }}
      >
        <ArrowBackIcon fontSize="large" />
      </button>
    </div>
  );
};

export default TournamentMenu;
