import React, { useContext, useState } from "react";
import { AuthContext } from "../AuthContext";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import "../css/login.css";
import LanguageSwitcher from "./LanguageSwitcher";

const Login = () => {

  const { t } = useTranslation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const response = await axios.post("https://localhost:8000/api/login/", {
        email: email,
        password: password,
      });
      login(response.data.user, response.data.access, response.data.refresh);
      navigate("/home");
    } catch (err) {
      console.error(err);
      setError(t('Invalid Credentials'));
    }
  };

  return (
    <div className="login-content">
      <LanguageSwitcher />
      <div className="login-container">
      <span style={{fontSize:"64px"}}>{t('login')}</span>
      <form onSubmit={handleSubmit} className="login-form">
        <div className="input-container">
          <label>{t('email')}</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value.replace(/[;/\\|<>]/g, ""))}
          />
        </div>
        <div className="input-container">
          <label>{t('Password')}</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">{t('Login')}</button>
      </form>
      {error && <p>{error}</p>}
      <Link to={"/reset_password"}>{t('Reset Password')}</Link>
      <Link to={"/register"}>{t('Register')}</Link>
      </div>
    </div>
  );
};

export default Login;
