import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "../css/history.css";
import GameDetails from "./GameDetails";
import { useTranslation } from "react-i18next";

const History = ({ id }) => {
    const { t } = useTranslation();
  const [history, setHistory] = useState([]);
  const [page, setPage] = useState(1);
  const [showMore, setShowMore] = useState(true);

  useEffect(() => {
    getHistory();
  }, [id]);

  const getHistory = async () => {
    try {
      const response = await axios.get(
        `https://localhost:8000/game/history/${id}/?page=1`
      );
      setHistory(response.data.results);
    } catch (error) {
      console.error(error);
    }
  };

  const SeeMore = async () => {
    try {
      const response = await axios.get(
        `https://localhost:8000/game/history/${id}/?page=${page + 1}`
      );
      setHistory((prevHistory) => [...prevHistory, ...response.data.results]);
      setPage(page + 1);
    } catch (error) {
      console.log("no more games");
      setShowMore(false);
    }
  };

  const Match = ({ game }) => {
    const [showDetails, setShowDetails] = useState(false);
    let result =
      game.player1.id == id
        ? game.score_player1 - game.score_player2
        : game.score_player2 - game.score_player1;
    return (
      <div className="match-container">
      <div className={`match ${result > 0 ? "win" : result < 0 ? "lose" : ""}`}>
        <Link to={`/profile/${game.player1.id}`} className="history-user">
          {game.player1.username}
        </Link>
        <div className="history-score">
          {game.score_player1} - {game.score_player2}
        </div>
        <Link to={`/profile/${game.player2.id}`} className="history-user">
          {game.player2.username}
        </Link>
        <div className="history-time">
          {new Date(game.time).toLocaleDateString()}
        </div>
        <div className="btn-match-details" onClick={() => setShowDetails(!showDetails)}>
          ...
        </div>
        
      </div>
      {showDetails && (
          <GameDetails game={game} />
        )}
      </div>
    );
  };

  if (history.length === 0) {
    return <div className="history">{t('No games played yet')}</div>;
  }

  return (
    <div className="history">
      {history.map((game, index) => (
        <Match key={index} game={game} />
      ))}
      {showMore && (
        <div className="history-see-more" onClick={SeeMore}>
          {t('See More')}
        </div>
      )}
    </div>
  );
};

export default History;
