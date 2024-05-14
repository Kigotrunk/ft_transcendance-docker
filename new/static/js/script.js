const short = document.querySelector('.short-menu');
const extanded = document.querySelector('.extanded-menu');
const phone = document.querySelector('.phone-menu');
const blured = document.querySelector('.blured');

const MenuPref = () => {
  const menuState = localStorage.getItem('menu');
  if (window.innerWidth > 1224) {
    if (menuState === 'short') {
      short.style.display = 'flex';
      extanded.style.display = 'none';
    }
    else if (menuState === 'extanded') {
      short.style.display = 'none';
      extanded.style.display = 'flex';
    }
  }
  else if (window.innerWidth < 768){
    short.style.display = 'none';
    extanded.style.display = 'none';
  }
  else {
    short.style.display = 'flex';
    extanded.style.display = 'none';
  }
}

MenuPref();
window.onresize = MenuPref;

const showMenu = () => {
  if (window.innerWidth < 1224) {
    phone.style.left = 0;
    blured.style.display = 'block';
    document.addEventListener('click', (event) => {
      const menuwidth = phone.offsetWidth;
      if (event.clientX > menuwidth) {
        phone.style.left = '-220px';
        blured.style.display = 'none';
      }
    });
  }
  else {
    if (short.style.display === 'none') {
      short.style.display = 'flex';
      extanded.style.display = 'none';
      localStorage.setItem('menu', 'short');
    }
    else {
      short.style.display = 'none';
      extanded.style.display = 'flex';
      localStorage.setItem('menu', 'extanded');
    }
  }
}

const showChat = (id) => {
  const content = document.querySelector('.content');
  fetch('get_chat/' + id)
  .then(response => response.text())
  .then(text => {
    const data = JSON.parse(text);
    console.log(data);
    let talkDiv = document.querySelector('.talk');
    if (!talkDiv) {
      talkDiv = document.createElement('div');
      talkDiv.classList.add('talk');
    }
    else 
      talkDiv.innerHTML = '';
    data.messages.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(message.issuer === data.other_user ? 'received' : 'send');
        messageDiv.textContent = message.message;
        talkDiv.appendChild(messageDiv);
    });
    // const messageForm = document.createElement('form');
    // messageForm.method = 'POST';
    // const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value; // Assuming CSRF token is available in the page
    // messageForm.innerHTML = `
    //     <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
    //     ${data.form}
    // `;
    // talkDiv.appendChild(messageForm);
    content.appendChild(talkDiv);
  });
}

const showChatList = () => {
  const content = document.querySelector('.content');
  fetch('chat_list')
    .then(response => response.text())
    .then(text => {
      const data = JSON.parse(text);
      console.log(data);
      const chatList = document.createElement('div');
        chatList.classList.add('chat-list');
        data.conversations.forEach(conversation => {
            const conversationLink = document.createElement('a');
            conversationLink.onclick = function () { showChat(conversation.id); };
            conversationLink.classList.add('chat-user');
            conversationLink.innerHTML = `
                <img src="" alt="profile picture">
                <h4>${conversation.other_user}</h4>
                <div class="overlay"></div>
            `;
            chatList.appendChild(conversationLink);
        });
        content.innerHTML = '';
        content.appendChild(chatList);
    });
}