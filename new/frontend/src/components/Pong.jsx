import React, { useEffect, useState, useRef } from 'react';

const PongGame = () => {
  const height = 600;
  const width = 800;
  const gameSocket = useRef(null);
  const [gameStarted, setGameStarted] = useState(false);
  const [score, setScore] = useState('');
  const canvasRef = useRef(null);
  const [up, setUp] = useState(false);
  const [down, setDown] = useState(false);

  useEffect(() => {
    gameSocket.current = new WebSocket('ws://' + window.location.host + `/ws/pong/`);

    gameSocket.current.onmessage = (e) => {
      const data = JSON.parse(e.data);
      console.log(data);
      if ('countdown' in data) {
        setScore(data['countdown']);
        if (data['countdown'] === "") {
          setGameStarted(true);
          setScore("0 - 0");
        }
      } else if ('waiting' in data && data['waiting'] === false) {
        setScore("0 - 0");
      } else {
        updateGameState(data);
      }
    };

    gameSocket.current.onopen = () => {
      console.error('gameSocket opened');
    };

    gameSocket.current.onclose = () => {
      console.error('gameSocket closed unexpectedly');
    };

    const handleKeyDown = (event) => {
      if (event.key === 'ArrowUp' && !up) {
        setUp(true);
        sendInput(1);
      } else if (event.key === 'ArrowDown' && !down) {
        setDown(true);
        sendInput(-1);
      }
    };

    const handleKeyUp = (event) => {
      if (event.key === 'ArrowUp') {
        setUp(false);
        sendInput(0);
      } else if (event.key === 'ArrowDown') {
        setDown(false);
        sendInput(0);
      }
    };

    const sendInput = (dir) => {
      if (!gameStarted) return;
      gameSocket.current.send(JSON.stringify({
        'action': 'move',
        'direction': dir,
      }));
    };

    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);

    window.addEventListener('blur', () => {
      sendInput(0);
    });

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('keyup', handleKeyUp);
      window.removeEventListener('blur', () => {
        sendInput(0);
      });
      gameSocket.current.close();
    };
  }, [gameStarted, up, down]);

  const updateGameState = (gameState) => {
    const ctx = canvasRef.current.getContext('2d');
    if ('game_over' in gameState && gameState['game_over'] === true) {
      return gameOver(gameState);
    }
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    drawBall(ctx, gameState.ball_position);
    ctx.fillRect(0, gameState.paddle1_position, 10, 80);
    ctx.fillRect(790, gameState.paddle2_position, 10, 80);
    if ('score' in gameState)
      setScore(`${gameState.score[0]} - ${gameState.score[1]}`);
    else if ('surv_score' in gameState)
      setScore(gameState['surv_score']);
  };

  const drawBall = (ctx, position) => {
    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(position[0], position[1], 10, 0, Math.PI * 2);
    ctx.fill();
  };

  const showGameMenu = () => (
    <div id="pong-menu">
      <button onClick={() => joinRoom('pvp', 'room1')}>Play Online</button>
      <button onClick={() => selectRoom()}>Play with a friend</button>
      <button onClick={() => versusAi()}>Ai Mode</button>
    </div>
  );

  const versusAi = () => (
    <div id="pong-menu">
      <button onClick={() => joinRoom('ai', 1)}>Easy</button>
      <button onClick={() => joinRoom('ai', 2)}>Medium</button>
      <button onClick={() => joinRoom('ai', 3)}>Hard</button>
      <button onClick={() => joinRoom('ai', 4)}>Survival</button>
    </div>
  );

  const selectRoom = () => (
    <div id="pong-menu">
      <button onClick={() => joinRoom('pvp', 'test 1')}>test 1</button>
      <button onClick={() => joinRoom('pvp', 'test 2')}>test 2</button>
      <input
        type="text"
        onKeyDown={(event) => {
          if (event.key === 'Enter') {
            joinRoom('pvp', event.target.value);
          }
        }}
      />
      <button onClick={() => joinRoom('pvp', document.querySelector('input').value)}>
        <span className="material-icons">send</span>
      </button>
    </div>
  );

  const joinRoom = (mode, roomName) => {
    console.log(`join in ${mode} room : ${roomName}`);
    gameSocket.current.send(JSON.stringify({
      'action': 'join',
      'mode': mode,
      'room': roomName
    }));
    document.getElementById('pong-menu').innerHTML = '';
  };

  const gameOver = (gameState) => (
    <div id="game-over">
      <span>GAME OVER</span>
      <div>
        <button className="primary-btn" onClick={() => joinRoom('ai', 4)}>Retry</button>
        <button className="secondary-btn" onClick={showGameMenu}>Return Menu</button>
      </div>
    </div>
  );

  return (
    <div id="game-container">
      <div id="score">{score}</div>
      <canvas id="pongCanvas" width={width} height={height} ref={canvasRef}></canvas>
      <div id="pong-menu">{showGameMenu()}</div>
    </div>
  );
};

export default PongGame;
