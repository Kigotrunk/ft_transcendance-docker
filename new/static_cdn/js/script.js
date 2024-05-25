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
  const chatContent = document.querySelector('.chat-content');
  let rightSection = document.querySelector('.chat-right-section');
    if (!rightSection) {
      rightSection = document.createElement('div');
      rightSection.classList.add('chat-right-section');
    }
    else 
      rightSection.innerHTML = '';

  fetch('/get_chat/' + id)
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
        messageDiv.classList.add(message.issuer === data.uid ? 'received' : 'send');
        messageDiv.textContent = message.message;
        talkDiv.appendChild(messageDiv);
    });
    const messageForm = document.createElement('form');
    messageForm.method = 'POST';
    messageForm.innerHTML = `
      <div class="input">
        <input type=\"text\" name=\"message\" class=\"text-input\" placeholder=\"Type a message\" autocomplete=\"off\" required id=\"id_message\">
        <button type="submit" class="send-button" disabled><span class="material-icons">send</span></button>
      </div>
    `
    rightSection.appendChild(talkDiv);
    rightSection.appendChild(messageForm);
    chatContent.appendChild(rightSection);
    talkDiv.scrollTop = talkDiv.scrollHeight;

    const button = document.querySelector('.send-button');
    const input = document.querySelector('.text-input');
    input.addEventListener('input', () => {
      if (input.value === '')
        button.disabled = true;
      else
        button.disabled = false;
    });
  });
}

const showChatList = () => {
  const content = document.querySelector('.content');
  const chatContent = document.createElement('div');
  chatContent.classList.add('chat-content');

  fetch('/chat_list')
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
                <img src="${conversation.other_user.pp}" alt="profile picture">
                <h4>${conversation.other_user.username}</h4>
                <div class="overlay"></div>
            `;
            chatList.appendChild(conversationLink);
        });
        content.innerHTML = '';
        chatContent.appendChild(chatList);
        content.appendChild(chatContent);
    });
}

const myProfile = () => {
const leftSection = document.createElement('div');
leftSection.classList.add('card', 'left-section');

const profilePicture = document.createElement('div');
profilePicture.classList.add('profile-picture');

const imgHover = document.createElement('div');
imgHover.classList.add('img-hover');
imgHover.innerHTML = '<span class="material-icons">edit</span>';

const profileImg = document.createElement('img');
// profileImg.src = request.user.profile_picture.url;
profileImg.alt = 'profile picture';

const username = document.createElement('h2');
// username.textContent = user.username;

profilePicture.appendChild(imgHover);
profilePicture.appendChild(profileImg);
leftSection.appendChild(profilePicture);
leftSection.appendChild(username);

const rightSection = document.createElement('div');
rightSection.classList.add('card', 'right-section');

const line1 = document.createElement('div');
line1.classList.add('line');

const winsInfo = document.createElement('div');
winsInfo.classList.add('info');
const winsTitle = document.createElement('h3');
winsTitle.textContent = 'WINS';
const winsValue = document.createElement('span');
winsValue.textContent = '10';
winsInfo.appendChild(winsTitle);
winsInfo.appendChild(winsValue);

const rankInfo = document.createElement('div');
rankInfo.classList.add('info');
const rankTitle = document.createElement('h3');
rankTitle.textContent = 'RANK';
const rankValue = document.createElement('span');
rankValue.textContent = 'Gold';
rankInfo.appendChild(rankTitle);
rankInfo.appendChild(rankValue);

line1.appendChild(winsInfo);
line1.appendChild(rankInfo);

const line2 = document.createElement('div');
line2.classList.add('line');

const globalInfo = document.createElement('div');
globalInfo.classList.add('info');
const globalTitle = document.createElement('h3');
globalTitle.textContent = 'GLOBAL';
const globalValue = document.createElement('span');
globalValue.textContent = '#1';
globalInfo.appendChild(globalTitle);
globalInfo.appendChild(globalValue);

const winsInfo2 = document.createElement('div');
winsInfo2.classList.add('info');
const winsTitle2 = document.createElement('h3');
winsTitle2.textContent = 'WINS';
const winsValue2 = document.createElement('span');
winsValue2.textContent = '10';
winsInfo2.appendChild(winsTitle2);
winsInfo2.appendChild(winsValue2);

line2.appendChild(globalInfo);
line2.appendChild(winsInfo2);

rightSection.appendChild(line1);
rightSection.appendChild(line2);

// Append the sections to the content div
const contentDiv = document.querySelector('.content');
contentDiv.innerHTML = '';
const profileDiv = document.createElement('div');
profileDiv.classList.add('profile-content');
profileDiv.appendChild(leftSection);
profileDiv.appendChild(rightSection);
contentDiv.appendChild(profileDiv);
}
