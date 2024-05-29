const content = document.querySelector('.content');

function fetchRooms() {
	// Simulate API call to fetch room list
	return ['room1', 'room2', 'room3'];
}

function displayRooms() {
	content.innerHTML = `
		<h1>Select a Room</h1>
		<ul id="room-list"></ul>
		<input id="room-name-input" type="text" placeholder="Room name">
		<button onclick="createRoom()">Create Room</button>
		<button onclick="versusAi()">AI Mode</button>
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

function versusAi() {
	content.innerHTML = `
		<div id="game-container">
			<div id="score">Connecting...</div>
			<canvas id="pongCanvas" width="600" height="600"></canvas>
		</div>
	`;

	const socket = new WebSocket('ws://' + window.location.host + `/ws/pong/ai/`);

	socket.onmessage = function(e) {
		const data = JSON.parse(e.data);
		console.log(data);
	};

	socket.onopen = function(e) {
		socket.send(JSON.stringify({ 'message': 'join' }));
	}

	const testButton = document.createElement('button');
	testButton.innerHTML = 'test'
	testButton.onclick = function() {
		console.log('send');
		socket.send(JSON.stringify({
			'message': 'hello'
		}));
	};
	content.appendChild(testButton);
}


///////////////		GAME	///////////////

const height = 600;
const width = 800;
const padLenght = 50;
const ballRadius = 5;

const joinRoom = (roomName) => {
	content.innerHTML = `
		<div id="game-container">
			<div id="score">Waiting for players...</div>
			<canvas id="pongCanvas" width="${width}" height="${height}"></canvas>
		</div>
	`;
	const canvas = document.getElementById('pongCanvas');
	const ctx = canvas.getContext('2d');
	ctx.fillStyle = "white";
	const scoreDiv = document.getElementById('score');
	let player = null;
	let localMode = roomName === 'local';
	let gameStarted = false;

	const socket = new WebSocket(
		'ws://' + window.location.host + `/ws/pong/${roomName}/`
	);

	socket.onmessage = function(e) {
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

	socket.onclose = function(e) {
		console.error('Chat socket closed unexpectedly');
	};
	
	let up = false;
	let down = false;

    function sendInput(dir) {
		if (!gameStarted)
			return;
        socket.send(JSON.stringify({
			'action': 'move',
			'player': player,
			'direction': dir,
		}));
	}

    document.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowUp' && up === false) {
            up = true;
			sendInput(up - down);
        }
		else if (event.key === 'ArrowDown' && down === false) {
            down = true;
			sendInput(up - down);
        }
    });

    document.addEventListener('keyup', (event) => {
		if (event.key === 'ArrowUp') {
            up = false;
			sendInput(up - down);
        }
		else if (event.key === 'ArrowDown') {
            down = false;
			sendInput(up - down);
        }
    });

	function updateGameState(gameState) {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		drawBall(gameState.ball_position);
		ctx.fillRect(0, gameState.paddle1_position, 10, 80);
		ctx.fillRect(790, gameState.paddle2_position, 10, 80);
		scoreDiv.innerText = `${gameState.score[0]} - ${gameState.score[1]}`;
	}

	function drawBall(position) {
		ctx.beginPath();
		ctx.arc(position[0], position[1], 10, 0, Math.PI * 2);
		ctx.fill();
	}

	socket.onopen = function(e) {
		socket.send(JSON.stringify({ 'action': 'join' }));
	}
}