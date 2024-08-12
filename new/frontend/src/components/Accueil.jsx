import React from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";


const Accueil = () => {
        const { t } = useTranslation();
  return (
    <div className="acceuil-container">
      <h1>{t('Accueil')}</h1>
      <div style={{display: "flex", flexDirection: "row", gap: "64px", marginBottom: "128px"}}>
        <Link to="/login">{t('Login')}</Link>
        <Link to="/register">{t('Register')}</Link>
      </div>
    </div>
  );
};

export default Accueil;
