import React from "react";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import axios from "axios";
import { useTranslation } from "react-i18next";
const VersusAiMenu = ({ setMenuState }) => {
    const { t } = useTranslation();
  const levels = ["Easy", "Medium", "Hard", "Survival"];

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

  return (
    <div className="game-menu">
      {levels.map((level, index) => (
        <button key={index} onClick={() => createAi(index + 1)}>
          {t(level)}
        </button>
      ))}
      <button className="btn-back" onClick={() => setMenuState("main")}>
        <ArrowBackIcon fontSize="large" />
      </button>
    </div>
  );
};

export default VersusAiMenu;
