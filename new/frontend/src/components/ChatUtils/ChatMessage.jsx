import React from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

const ChatMessage = ({ message, user }) => {
    const { t } = useTranslation();
  if (message.message.startsWith("/invite ")) {
    return (
      <div
        className={`invite ${
          message.issuer.username === user.username ? "sent" : "received"
        }`}
      >
        <span>{message.issuer.username} {t('wants to play')} !</span>
        <Link to={`/game/${message.message.split(" ")[1]}`}>{t('Join')}</Link>
      </div>
    );
  } else if (message.message.startsWith("/friend_request ")) {
    return (
      <div
        className={`friend-request ${
          message.issuer.username === user.username ? "sent" : "received"
        }`}
      >
        <span>{message.issuer.username} {t('sends a friend request')}</span>
      </div>
    );
  }

  return (
    <div
      className={`chat-message ${
        message.issuer.username === user.username ? "sent" : "received"
      }`}
    >
      {message.message}
    </div>
  );
};

export default ChatMessage;
