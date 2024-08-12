import React from "react";
import { useTranslation } from "react-i18next";

const MainMenu = ({ setMenuState }) => {
    const { t } = useTranslation();
  return (
    <div id="game-main-menu">
      <button onClick={() => setMenuState("duel")}>{t('Duel')}</button>
      <button onClick={() => setMenuState("tournament")}>{t('Tournament')}</button>
      <button onClick={() => setMenuState("ai")}>{t('Play AI')}</button>
    </div>
  );
};

export default MainMenu;
