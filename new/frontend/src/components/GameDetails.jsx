import React from 'react'

const GameStats = ({ game }) => {
  console.log(game)
  return (
  <div className="game-details">
    {game.order_points_scored.map((player, index) => (
      <div key={index}>
        {game.nb_echange_per_point[index] + "echanges"}{" - "}
        {player == game.player1.id ? game.player1.username + " scored" : game.player2.username + " scored"}
      </div>
    ))}
  </div>
  )
}

export default GameStats