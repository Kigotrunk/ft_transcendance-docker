import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../../AuthContext";
import axios from "axios";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import { useTranslation } from "react-i18next";

const GameResult = ({ gameResult, setMenuState }) => {
    const { t } = useTranslation();
  const { user } = useContext(AuthContext);
  const [winnerProfile, setWinnerProfile] = useState({});
  const [loserProfile, setLoserProfile] = useState({});

  const getWinnerProfile = async (id) => {
    try {
      const response = await axios.get(
        `https://localhost:8000/api/profile/${id}/`
      );
      setWinnerProfile(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const getLoserProfile = async (id) => {
    try {
      const response = await axios.get(
        `https://localhost:8000/api/profile/${id}/`
      );
      console.log(response.data);
      setLoserProfile(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const createAi = async (level) => {
    try {
      const response = await axios.post(
        `https://localhost:8000/game/create_ai/?diff=${level}`
      );
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  if (gameResult["mode"] === "ia") {
    return (
      <div className="game-result">
        <h2>{t('Game Over')}</h2>
        <span>{gameResult["win"] ? t("You win") : t("You lose")}</span>
        <span>{t('Score')}: {gameResult["score"]}</span>
        <button onClick={() => createAi(gameResult["diff"])}>{t('Play again')}</button>
        <button onClick={() => setMenuState("main")}>{t('Back to main menu')}</button>
      </div>
    );
  }

  useEffect(() => {
    if ("winner" in gameResult) getWinnerProfile(gameResult["winner"]);
    if ("loser" in gameResult) getLoserProfile(gameResult["loser"]);
  }, []);

  return (
    <div className="game-result">
      <div>{t('Score')}: {gameResult["score"]}</div>
      <div>{gameResult["winner"] == user.id ? t('You win') : t('You lose')}</div>
      <div className="result-users">
        <div className="result-user">
          <span>{winnerProfile.username}</span>
          <span>{winnerProfile.elo}</span>
          <TrendingUpIcon />
        </div>
        <div className="result-user">
          <span>{loserProfile.username}</span>
          <span>{loserProfile.elo}</span>
          <TrendingDownIcon />
        </div>
      </div>
      {gameResult["mode"] === "cup" && gameResult["winner"] == user.id ? (
        t('You advance to the next round')
      ) : (
        <button onClick={() => setMenuState("main")}>{t('Back to main menu')}</button>
      )}
    </div>
  );
};

export default GameResult;
