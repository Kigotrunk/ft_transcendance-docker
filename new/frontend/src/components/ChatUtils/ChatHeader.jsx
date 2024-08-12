import React, { useContext, useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import BlockIcon from "@mui/icons-material/Block";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import GamepadIcon from "@mui/icons-material/Gamepad";
import CancelIcon from "@mui/icons-material/Cancel";
import axios from "axios";
import { AuthContext } from "../../AuthContext";
import PersonAddDisabledIcon from "@mui/icons-material/PersonAddDisabled";
import { useTranslation } from "react-i18next";

const ChatHeader = ({ user2, isBlocked, setIsBlocked }) => {
    const [showAddButton, setShowAddButton] = useState(false);
    const { t } = useTranslation();
  const [friendStatus, setFriendStatus] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState(false);
  const [inGame, setInGame] = useState(false);
  const [showResponse, setShowResponse] = useState(false);
  const { user, chatSocketRef } = useContext(AuthContext);
  const navigate = useNavigate();

  const getFriendStatus = async () => {
    try {
      const response = await axios.get(
        `https://localhost:8000/friend_status/?friend_id=${user2.id}`
      );
      if (response.data.friendStatus === "none") {
        setShowAddButton(true);
      } else if (response.data.friendStatus === "friends") {
        setFriendStatus(true);
      } else if (response.data.friendStatus === "received") {
        setShowResponse(true);
        setShowAddButton(false);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const getConnectionStatus = async () => {
    try {
      const response = await axios.get(
        `https://localhost:8000/connection_status/${user2.id}/`
      );
      console.log(response.data);
      setFriendStatus(response.data.is_friend);
      setConnectionStatus(response.data.is_connected);
      setInGame(response.data.is_in_game);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    getFriendStatus();
    getConnectionStatus();
  }, [user2]);

  const addFriend = async () => {
    try {
      const response = await axios.post(
        `https://localhost:8000/send_invitation/?receiver_id=${user2.id}`
      );
      console.log(response.data);
      chatSocketRef.current.send(
        JSON.stringify({
          message: `/friend_request ${user2.id}`,
          issuer: user.username,
          receiver: user2.username,
        })
      );
      setShowAddButton(false);
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

  const blockUser = async () => {
    try {
      const response = await axios.post(
        `https://localhost:8000/block_user/?blocked_id=${user2.id}`
      );
      console.log(response.data);
      setIsBlocked(true);
    } catch (error) {
      console.error(error);
    }
  };

  const unblockUser = async () => {
    try {
      const response = await axios.post(
        `https://localhost:8000/block_user/?blocked_id=${user2.id}&unblock=true`
      );
      console.log(response.data);
      setIsBlocked(false);
    } catch (error) {
      console.error(error);
    }
  };

  const acceptRequest = async () => {
    try {
      const response = await axios.post(
        `https://localhost:8000/respond_invitation/?sender_id=${user2.id}&action=accept`
      );
      console.log(response.data);
      setShowResponse(false);
      setFriendStatus(true);
    } catch (error) {
      console.error(error);
    }
  };

  const rejectRequest = async () => {
    try {
      const response = await axios.post(
        `https://localhost:8000/respond_invitation/?sender_id=${user2.id}&action=reject`
      );
      console.log(response.data);
      setShowResponse(false);
      setShowAddButton(true);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="chat-header">
      <div className="chat-header-user">
        <Link to={`/profile/${user2.id}`}>
          <div className="chat-header-pic">
            <img
              src={`https://localhost:8000${user2.profile_picture}`}
              alt="profile picture"
            />
            {friendStatus && (
              inGame ? (
                <div className="in-game-led"></div>
              ) : (
                connectionStatus ? (
                  <div className="online-led"></div>
                ) : (
                  <div className="offline-led"></div>
                )
              )
            )}
          </div>
          <span>{user2.username}</span>
        </Link>
        {showAddButton && (
          <div
            className="btn btn-primary"
            title={t('Add friend')}
            onClick={addFriend}
          >
            <PersonAddIcon fontSize="small" />
          </div>
        )}
        {showResponse && (
          <>
            <div
              className="btn btn-primary"
              title={t('Accept friend request')}
              onClick={acceptRequest}
            >
              <PersonAddIcon fontSize="small" />
            </div>
            <div
              className="btn"
              title={t('Reject friend request')}
              onClick={rejectRequest}
            >
              <PersonAddDisabledIcon fontSize="small" />
            </div>
          </>
        )}
      </div>
      <div className="chat-header-actions">
        {friendStatus && (
          <div
            className="btn btn-primary"
            title={t('Invite in game')}
            onClick={inviteInGame}
          >
            <GamepadIcon fontSize="small" />
            <span>{t('Invite in game')}</span>
          </div>
        )}
        {isBlocked ? (
          <div className="btn" title={t('Unblock user')} onClick={unblockUser}>
            <CancelIcon fontSize="small" />
          </div>
        ) : (
          <div className="btn" title={t('Block user')} onClick={blockUser}>
            <BlockIcon fontSize="small" />
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatHeader;
