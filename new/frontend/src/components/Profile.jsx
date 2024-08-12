import React, { useEffect, useState, useContext } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../AuthContext";
import axios from "axios";
import History from "./History";
import "../css/profile.css";
import ProfileActions from "./ProfileUtils.jsx/ProfileActions";
import { useTranslation } from "react-i18next";
import LanguageSwitcher from "./LanguageSwitcher";

const Profile = () => {
  const { t } = useTranslation();
  const { id } = useParams();
  const { user } = useContext(AuthContext);
  const [profile, setProfile] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState(false);
  const [inGame, setInGame] = useState(false);
  const [enableEdit, setEnableEdit] = useState(false);
  const navigate = useNavigate();

  const isMyProfile = id == user.id;

  const getProfile = async () => {
    try {
      const response = await axios.get(
        `https://localhost:8000/api/profile/${id}/`
      );
      console.log(response.data);
      setProfile(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const getConnectionStatus = async () => {
    try {
      const response = await axios.get(
        `https://localhost:8000/connection_status/${id}/`
      );
      console.log(response.data);
      setConnectionStatus(response.data.is_connected);
      setInGame(response.data.is_in_game);
      console.log(response.data.is_in_game);
    } catch (error) {
      console.error(error);
    }
  };

  const getQueueStatus = async () => {
    try {
      const response = await axios.get(
        `https://localhost:8000/game/status/`
      );
      console.log(response.data);
      if (!response.data["in_queue"] && !response.data["in_queue_cup"] && !response.data["in_cup"] && !response.data["in_lobby"]) {
        setEnableEdit(true);
      }
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    window.scrollTo(0, 0);
    getProfile();
    getConnectionStatus();
    getQueueStatus();
  }, [id]);

  if (!profile) {
    return <div>Loading...</div>;
  }

  return (
    <div className="profile-content">
      <LanguageSwitcher />
      <div className="profile-card">
        <div className="profile-picture">
          {isMyProfile && (
            <div
              className="img-hover"
              onClick={() => enableEdit && navigate("/profileedit")}
            >
              <span className="material-icons">edit</span>
            </div>
          )}
          <img
            src={`https://localhost:8000${profile.profile_picture}`}
            alt="profile picture"
          />
        </div>
        <div className="profile-info">
          <div className="profile-upper-line">
            <span>{profile.username}</span>
            {isMyProfile ? (
              <Link className={`btn-grey ${enableEdit ? '' : 'btn-disabled'}`} to={enableEdit ? "/profileedit" : "#"} title={enableEdit ? "Edit profile" : "You can't edit your profile while in a game or in queue"}>
                {t('Edit Profile')}
              </Link>
            ) : (
              <ProfileActions user2={profile} />
            )}
          </div>
          <div>
            <p>
              {profile.nb_win} {t('Wins')} - {profile.nb_top1} {t('Cup Wins')} - {profile.elo}{" "}
              LP
            </p>
            {inGame ? <p>{t('In Game')}</p> : connectionStatus && <p>{t('Online')}</p>}
          </div>
        </div>
      </div>
      <div className="divider"></div>
      <History id={profile.id} />
    </div>
  );
};

export default Profile;
