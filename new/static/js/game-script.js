function fetchRooms() {
	// Simulate API call to fetch room list
	return ['room1', 'room2', 'room3'];
}

function displayRooms() {
	const content = document.querySelector('.content');
	content.innerHTML = `
		<h1>Select a Room</h1>
		<ul id="room-list"></ul>
		<input id="room-name-input" type="text" placeholder="Room name">
		<button onclick="createRoom()">Create Room</button>
		<button onclick="joinLocal()">Local Mode</button>
	`;

	const rooms = fetchRooms();
	const roomList = document.getElementById('room-list');
	roomList.innerHTML = '';
	rooms.forEach(room => {
		const li = document.createElement('li');
		li.textContent = room;
		li.onclick = () => joinRoom(room);
		roomList.appendChild(li);
	});
}

function createRoom() {
	const roomName = document.getElementById('room-name-input').value;
	if (roomName) {
		joinRoom(roomName);
	}
}

function joinLocal() {
	window.location.href = `/game/local/`;
}


//////////////////////////////


const joinRoom = (roomName) => {
	const content = document.querySelector('.content');
	content.innerHTML = `
		<div id="game-container">
			<div id="score">Waiting for players...</div>
			<canvas id="pongCanvas" width="600" height="600"></canvas>
		</div>
	`
	const canvas = document.getElementById('pongCanvas');
	const ctx = canvas.getContext('2d');
	ctx.fillStyle = "white";
	const scoreDiv = document.getElementById('score');
	let player = null;
	let localMode = roomName === 'local';
	let gameStarted = false;

	const chatSocket = new WebSocket(
		'ws://' + window.location.host + `/ws/pong/${roomName}/`
	);

	chatSocket.onmessage = function(e) {
		const data = JSON.parse(e.data);
		if ('player' in data) {
			player = data['player'];
		} else if ('countdown' in data) {
			scoreDiv.innerText = data['countdown'];
			if (data['countdown'] === "") {
				gameStarted = true;
				scoreDiv.innerText = "0 - 0";
			}
		} else if ('waiting' in data && data['waiting'] === false) {
			// Mettre à jour l'affichage lorsque les deux joueurs sont connectés
			scoreDiv.innerText = "0 - 0";
		} else {
			updateGameState(data);
		}
	};

	chatSocket.onclose = function(e) {
		console.error('Chat socket closed unexpectedly');
	};

	document.addEventListener('keydown', function(event) {
		if (!gameStarted) return;

		if (localMode) {
			// Local mode controls
			if (event.key === 'w' || event.key === 'W') {
				movePaddle('left', -5);
			} else if (event.key === 's' || event.key === 'S') {
				movePaddle('left', 5);
			} else if (event.key === 'ArrowUp') {
				movePaddle('right', -5);
			} else if (event.key === 'ArrowDown') {
				movePaddle('right', 5);
			}
		} else {
			// Online mode controls
			if (event.key === 'ArrowUp') {
				movePaddle(player, -5);
			}
			else if (event.key === 'ArrowDown') {
				movePaddle(player, 5);
			}
		}
	});

	function movePaddle(player, delta) {
		chatSocket.send(JSON.stringify({
			'action': 'move',
			'player': player,
			'delta': delta
		}));
	}

	function updateGameState(gameState) {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		drawBall(gameState.ball_position);
		drawPaddle(gameState.paddle1_position, 10);
		drawPaddle(gameState.paddle2_position, canvas.width - 20);
		scoreDiv.innerText = `${gameState.score[0]} - ${gameState.score[1]}`;
	}

	function drawBall(position) {
		ctx.beginPath();
		ctx.arc(position[0] * 6, position[1] * 6, 10, 0, Math.PI * 2);
		ctx.fill();
	}

	function drawPaddle(position, x) {
		ctx.fillRect(x, position * 6 - 40, 10, 80);
	}

	chatSocket.onopen = function(e) {
		chatSocket.send(JSON.stringify({ 'action': 'join' }));
	}
}
