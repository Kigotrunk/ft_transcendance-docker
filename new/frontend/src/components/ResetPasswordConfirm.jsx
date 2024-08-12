import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";

const ResetPasswordConfirm = () => {
    const { t } = useTranslation();
  const { uid, token } = useParams();
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [error, setError] = useState("");
  const [csrfToken, setCsrfToken] = useState("");

  useEffect(() => {
    const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfTokenMeta) {
      setCsrfToken(csrfTokenMeta.getAttribute("content"));
    }
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    try {
      const response = await axios.post(
        `https://localhost:8000/api/reset_password_confirm/`,
        {
          uidb64: uid,
          token: token,
          password: password,
          password2: password2,
        },
        {
          headers: {
            "X-CSRFToken": csrfToken,
          },
        }
      );
    } catch (err) {
      console.error(err);
      setError(t("Failed to reset password"));
    }
  };

  return (
    <div>
      <h2>{('Reset Password')}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>{t('New Password')}:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div>
          <label>{t('Confirm New Password')}:</label>
          <input
            type="password"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
          />
        </div>
        <button type="submit">{t('Reset Password')}</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  );
};

export default ResetPasswordConfirm;
