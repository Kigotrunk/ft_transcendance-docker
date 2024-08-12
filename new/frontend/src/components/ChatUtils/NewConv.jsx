import React, { useState, useContext } from "react";
import { AuthContext } from "../../AuthContext";
import { useTranslation } from "react-i18next";

const NewConv = ({ setNewConv, getConversations }) => {
  const [newUser, setNewUser] = useState("");
  const [messageInput, setMessageInput] = useState("");
  const [error, setError] = useState("");
  const { user, chatSocketRef } = useContext(AuthContext);
  const { t } = useTranslation();

  const createConv = (e) => {
    e.preventDefault();
    if (messageInput.trim() === "") {
      setError(t('Message cannot be empty'));
      return;
    }
    chatSocketRef.current.send(
      JSON.stringify({
        type: "message",
        issuer: user.username,
        receiver: newUser,
        message: messageInput,
      })
    );
    getConversations();
    setNewConv(false);
  };

  const handleClickOutside = () => {
    setNewConv(false);
  };

  const handleClickForm = (e) => {
    e.stopPropagation();
  };

  return (
    <div className="backdrop" onClick={handleClickOutside}>
      <form
        onSubmit={createConv}
        className="new-conv-form"
        onClick={handleClickForm}
      >
        <input
          type="text"
          placeholder={t('Username')}
          value={newUser}
          onChange={(e) => setNewUser(e.target.value.replace(/[;/\\|<>]/g, ""))}
        /> 
        <input
          type="text"
          placeholder="Message"
          value={messageInput}
          onChange={(e) =>
            setMessageInput(e.target.value.replace(/[;/\\|<>]/g, ""))
          }
        />
        <button type="submit">{t('Send')}</button>
        <p>{error}</p>
      </form>
    </div>
  );
};

export default NewConv;
