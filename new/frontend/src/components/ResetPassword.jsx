import React, { useContext, useState } from "react";
import { AuthContext } from "../AuthContext";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

const ResetPassword = () => {
    const { t } = useTranslation();
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleReset = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const response = await axios.post(
        "https://localhost:8000/api/reset_password/",
        {
          email: email,
        }
      );
    } catch (err) {
      console.error(err);
      setError(t('Invalid Credentials'));
    }
  };

  return (
    <div>
      <h2>{t('Reset Password')}</h2>
      <form onSubmit={handleReset}>
        <div>
          <label>Email:</label>
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <button type="submit">{t('Send Email')}</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  );
};

export default ResetPassword;
