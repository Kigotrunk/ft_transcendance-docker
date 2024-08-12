// i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import HttpApi from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

// Initialize i18next
i18n
  .use(HttpApi) // Load translations from the backend
  .use(LanguageDetector) // Detect user language
  .use(initReactI18next) // Bind react-i18next to i18next
  .init({
    fallbackLng: 'en', // Default language
    debug: true, // Enable debug mode

    interpolation: {
      escapeValue: false, // React already safely escapes
    },
    backend: {
      loadPath: '/locales/{{lng}}/translation.json', // Path to your translation files
    },
  });

export default i18n;