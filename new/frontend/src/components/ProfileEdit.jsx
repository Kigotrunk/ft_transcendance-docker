import React, { useContext } from "react";
import { useState } from "react";
import { AuthContext } from "../AuthContext";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

const ProfileEdit = () => {
    const { t } = useTranslation();
    const { user, refreshUser, gameSocketRef } = useContext(AuthContext);
  const navigate = useNavigate();
  const [username, setUsername] = useState(user.username);
  const [usernameError, setUsernameError] = useState("");
  const [profilePicture, setProfilePicture] = useState(null);
  const [profilePictureError, setProfilePictureError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append("username", username);
      if (profilePicture) {
        formData.append("profile_picture", profilePicture);
      }
      await axios.put(
        `https://localhost:8000/api/profile/${user.id}/`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      await refreshUser();
      await axios.post(`https://localhost:8000/game/update_user/`, {
        name: username,
      });
      navigate(`/profile/${user.id}`);
    } catch (error) {
      console.error(error);
      if (error.response.data.username) {
        setUsernameError(error.response.data.username[0]);
      }
      if (error.response.data.profile_picture) {
        setProfilePictureError(error.response.data.profile_picture[0]);
      }
    }
  };

  return (
    <div className="profile-edit">
      <form onSubmit={handleSubmit}>
        <label htmlFor="username">{t('Username')}</label>
        <input
          id="username"
          type="text"
          autoComplete="off"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value.replace(/[;/\\|<>]/g, ""))
          }
        />
        <span className="error">{usernameError}</span>

        <label htmlFor="profile_picture">{t('Profile Picture')}</label>
        <input
          id="username"
          type="file"
          onChange={(e) => setProfilePicture(e.target.files[0])}
        />
        <span className="error">{profilePictureError}</span>

        <button type="submit">{t('Save')}</button>
      </form>
    </div>
  );
};

export default ProfileEdit;
