import React from "react";
import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import "../css/login.css";
import { useTranslation } from "react-i18next";

const Register = () => {
    const { t } = useTranslation();
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const handleFormValidation = (e) => {
    e.preventDefault();
    // if (password1 !== password2) {
    //   setMessage("Passwords do not match");
    //   return;
    // }
    axios
      .post("https://localhost:8000/api/register/", {
        email: email,
        username: username,
        password1: password1,
        password2: password2,
      })
      .then((response) => {
        setMessage(response.data.message);
        navigate("/login");
      })
      .catch((error) => {
        if (error.response && error.response.data) {
            const errorData = error.response.data;
            let errorMessage = "";
    
            if (errorData.email) {
              errorMessage += t(errorData.email) + " ";
            }
            else if (errorData.invalid_email_format) {
              errorMessage += t(errorData.invalid_email_format) + " ";
            }
            else if (errorData.username) {
                errorMessage += t(errorData.username) + " ";
            }
            else if (errorData.password_mismatch) {
                errorMessage += t(errorData.password_mismatch) + " ";
            }
            else if (errorData.password_errors) {
                errorMessage += errorData.password_errors.map((msg) => t(msg)).join(' ') + " ";
            }
            setMessage(errorMessage.trim());
        } else {
            setMessage(t("Error connecting to the server. Please try again."));
        }
    });
  };

  return (
    <div className="login-content">
      <div className="login-container">
      <span style={{fontSize:"64px"}}>{t('Register')}</span>
      <form className="register-form" onSubmit={handleFormValidation}>
      <div className="input-container">
        <label>Email</label>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        </div>
        <div className="input-container">
        <label>{t('Username')}</label>
        <input
          type="text"
          placeholder={t('Username')}
          value={username}
          onChange={(e) =>
            setUsername(e.target.value.replace(/[;/\\|<>]/g, ""))
          }
        />
        </div>
        <div className="input-container">
        <label>{t('Password')}</label>
        <input
          type="password"
          placeholder={t('Password')}
          value={password1}
          onChange={(e) => setPassword1(e.target.value)}
        />
        </div>
        <div className="input-container">
        <label>{t('Confirm password')}</label>
        <input
          type="password"
          placeholder={t('Confirm password')}
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
        />
        </div>
        <button type="submit">{t('Register')}</button>
      </form>
      {message && <p>{message}</p>}
      <Link to="/login">{t('Login')}</Link>
    </div>
    </div>
  );
};

export default Register;
