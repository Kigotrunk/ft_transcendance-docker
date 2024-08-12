import React from 'react';
import { useTranslation } from 'react-i18next';

const LanguageSwitcher = () => {
  const { i18n } = useTranslation();

  const handleLanguageChange = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <div className="language-switcher">
      <button onClick={() => handleLanguageChange('en')}>EN</button>
      <button onClick={() => handleLanguageChange('fr')}>FR</button>
    </div>
  );
};

export default LanguageSwitcher;