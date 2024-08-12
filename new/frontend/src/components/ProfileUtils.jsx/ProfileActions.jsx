import React, { useEffect, useState, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import BlockIcon from "@mui/icons-material/Block";
import SportsEsportsIcon from "@mui/icons-material/SportsEsports";
import PersonRemoveIcon from "@mui/icons-material/PersonRemove";
import ChatIcon from "@mui/icons-material/Chat";
import { AuthContext } from "../../AuthContext";
import { useTranslation } from "react-i18next";

const ProfileActions = ({ user2 }) => {
    const { t } = useTranslation();
  const navigate = useNavigate();
  const { user, chatSocketRef } = useContext(AuthContext);
  const [friendStatus, setFriendStatus] = useState("");

  useEffect(() => {
    getFriendStatus();
  }, [user2.id]);

  const getFriendStatus = async () => {
    try {
      const response = await axios.get(
        `https://localhost:8000/friend_status/?friend_id=${user2.id}`
      );
      setFriendStatus(response.data.friendStatus);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const sendRequest = async () => {
    try {
      await axios.post(
        `https://localhost:8000/send_invitation/?receiver_id=${user2.id}`
      );
      chatSocketRef.current.send(
        JSON.stringify({
          message: `/friend_request ${user2.id}`,
          issuer: user.username,
          receiver: user2.username,
        })
      );
      setFriendStatus("sent");
    } catch (error) {
      console.error(error);
    }
  };

  const inviteInGame = () => {
    const gameId = `${user.id}-${user2.id}`;
    chatSocketRef.current.send(
      JSON.stringify({
        message: `/invite ${gameId}`,
        issuer: user.username,
        receiver: user2.username,
      })
    );
    navigate(`/game/${gameId}`);
  };

  const acceptRequest = async () => {
    try {
      const response = await axios.post(
        `https://localhost:8000/respond_invitation/?sender_id=${user2.id}&action=accept`
      );
      setFriendStatus("friends");
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const rejectRequest = async () => {
    try {
      const response = await axios.post(
        `https://localhost:8000/respond_invitation/?sender_id=${user2.id}&action=reject`
      );
      setFriendStatus("none");
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const GoToChat = async () => {
    try {
      const response = await axios.get(
        `https://localhost:8000/ask_cid/?user2_id=${user2.id}`
      );
      if ("id" in response.data && response.data.id) {
        navigate(`/chat/${response.data.id}`);
      } else {
        navigate(`/chat/`);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const removeFriend = async () => {
    try {
      const response = await axios.post(
        `https://localhost:8000/remove_friend/?friend_id=${user2.id}`
      );
      console.log(response.data);
      setFriendStatus("none");
    } catch (error) {
      console.error(error);
    }
  };

  if (!friendStatus) {
    return null;
  }

  if (friendStatus == "friends") {
    return (
      <>
        <div className="profile-actions">
          <div
            className="btn btn-primary"
            title={t('Invite in game')}
            onClick={inviteInGame}
          >
            <SportsEsportsIcon fontSize="small" />
          </div>

          <div className="btn" title={t('Go to chat')} onClick={GoToChat}>
            <ChatIcon fontSize="small" />
          </div>
          <div className="btn" title={t('Remove friend')} onClick={removeFriend}>
            <PersonRemoveIcon fontSize="small" />
          </div>
        </div>
      </>
    );
  }

  if (friendStatus == "received") {
    return (
      <div className="profile-actions">
        <div
          className="btn btn-primary"
          title={t('Accept friend request')}
          onClick={acceptRequest}
        >
          <PersonAddIcon fontSize="small" />
        </div>

        <div
          className="btn"
          title={t('Decline friend request')}
          onClick={rejectRequest}
        >
          <BlockIcon fontSize="small" />
        </div>

        <div className="btn" title={t('Go to chat')} onClick={GoToChat}>
          <ChatIcon fontSize="small" />
        </div>
      </div>
    );
  }

  if (friendStatus == "sent") {
    return (
      <div className="profile-actions">
        <div className="btn" title={t('Go to chat')} onClick={GoToChat}>
          <ChatIcon fontSize="small" />
        </div>
      </div>
    );
  }

  if (friendStatus == "none") {
    return (
      <div className="profile-actions">
        <div
          className="btn btn-primary"
          title="Add friend"
          onClick={sendRequest}
        >
          <PersonAddIcon fontSize="small" />
        </div>

        <div className="btn" title={t('Go to chat')} onClick={GoToChat}>
          <ChatIcon fontSize="small" />
        </div>
      </div>
    );
  }

  return null;
};

export default ProfileActions;
