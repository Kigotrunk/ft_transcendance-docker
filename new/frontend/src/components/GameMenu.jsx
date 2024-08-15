import {
  MainMenu,
  VersusAiMenu,
  TournamentMenu,
  WaitingDuelMenu,
  GameResult,
} from "./GameMenuUtils";
import { useTranslation } from "react-i18next";

const GameMenu = ({ menuState, setMenuState, countdown, gameResult, setLobbyState }) => {
  const { t } = useTranslation();
  const getMenuState = () => {
    if (menuState === "") {
      return null;
    } else if (menuState === "main") {
      return <MainMenu setMenuState={setMenuState} />;
    } else if (menuState === "ai") {
      return <VersusAiMenu setMenuState={setMenuState} />;
    } else if (menuState === "tournament") {
      return <TournamentMenu setMenuState={setMenuState} queueState={false} setLobbyState={setLobbyState} />;
    } else if (menuState === "duel") {
      return <WaitingDuelMenu setMenuState={setMenuState} queueState={false} />;
    } else if (menuState === "cup-waiting") {
      return <div>{t('Waiting for the next match')}</div>;
    } else if (menuState === "countdown") {
      return <div style={{ fontSize: "64px" }}>{countdown}</div>;
    } else if (menuState === "cup-loser") {
      return <div>{t('You lost the cup')}</div>;
    } else if (menuState === "cup-winner") {
      return <div>{t('Congratulations! You won the cup')}</div>;
    } else if (menuState === "match-result") {
      return <GameResult gameResult={gameResult} setMenuState={setMenuState} />;
    } else if (menuState === "waiting-opponent") {
      return <div>{t('Waiting for opponent...')}</div>;
    } else if (menuState === "in-queue") {
      return <WaitingDuelMenu setMenuState={setMenuState} queueState={true} />;
    } else if (menuState === "cup-queue") {
      return <TournamentMenu setMenuState={setMenuState} queueState={true} setLobbyState={setLobbyState} />;
    }
    return null;
  };

  return <div className="game-menu">{getMenuState()}</div>;
};

export default GameMenu;
