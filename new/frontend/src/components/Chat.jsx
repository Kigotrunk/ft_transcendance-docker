import React, { useState, useEffect } from 'react';
import '../css/chat.css';

const Chat = () => {
  const [conversations, setConversations] = useState([]);
  const [messages, setMessages] = useState([]);
  const [selectedChatId, setSelectedChatId] = useState(null);
  const [messageInput, setMessageInput] = useState('');

  useEffect(() => {
    // Fetch chat list
    fetch('http://localhost:8000/chat_list')
      .then(response => {console.log(response); response.json()})
      .then(data => {
        setConversations(data.conversations);
      })
      .catch(error => {
        console.error('Error fetching chat list:', error);
      });
  }, []);

  useEffect(() => {
    // Fetch chat messages when selectedChatId changes
    if (selectedChatId) {
      fetch(`http://localhost:8000/get_chat/${selectedChatId}`)
        .then(response => response.json())
        .then(data => {
          setMessages(data.messages);
        })
        .catch(error => {
          console.error('Error fetching chat:', error);
        });
    }
  }, [selectedChatId]);

  const showChat = (id) => {
    setSelectedChatId(id);
  };

  const sendMessage = (e) => {
    e.preventDefault();
    const message = messageInput.trim();
    if (message !== '') {
      // Implement sending message logic here
      setMessageInput('');
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-list">
        {conversations.map(conversation => (
          <div key={conversation.id} className="chat-user" onClick={() => showChat(conversation.id)}>
            <img src={conversation.other_user.pp} alt="profile picture" />
            <h4>{conversation.other_user.username}</h4>
            <div className="overlay"></div>
          </div>
        ))}
      </div>
      { selectedChatId ? (
      <div className="chat-content">
        <div className="chat-right-section">
          <div className="talk">
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.issuer === data.uid ? 'received' : 'send'}`}>
                {message.message}
              </div>
            ))}
          </div>
          <form onSubmit={sendMessage} className="message-form">
            <div className="input">
              <input
                type="text"
                className="text-input"
                placeholder="Type a message"
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                autoComplete="off"
                required
              />
              <button type="submit" className="send-button" disabled={messageInput.trim() === ''}>
                <span className="material-icons">send</span>
              </button>
            </div>
          </form>
        </div>
      </div> ) : null}
    </div>
  );
};

export default Chat;
