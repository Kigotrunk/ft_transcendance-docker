import React from "react";
import Chart from "chart.js/auto";
import { Bar } from "react-chartjs-2";
import "../css/stats.css";
import { useTranslation } from "react-i18next";

const GameStats = ({ game, uid }) => {
  const { t } = useTranslation();

  const labels = game.nb_echange_per_point.map(
    (_, index) => `${game.nb_echange_per_point[index]} echanges`
  );
  const data = game.nb_echange_per_point.map((value) => value || 0.1);
  const backgroundColor = game.order_points_scored.map((player) =>
    player == uid ? "blue" : "red"
  );

  return (
    <div className="game-details">
      <Bar
        data={{
          labels: labels,
          datasets: [
            {
              data: data,
              backgroundColor: backgroundColor,
              borderColor: backgroundColor,
              borderWidth: 1,
            },
          ],
        }}
        options={{
          scales: {
            y: {
              beginAtZero: true,
            },
            x: {
              display: false,
            },
          },
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              callbacks: {
                label: (tooltipItem) => {
                  const player =
                    game.order_points_scored[tooltipItem.dataIndex] ==
                    game.player1.id
                      ? game.player1.username
                      : game.player2.username;
                  return player + " " + t("scored");
                },
              },
            },
          },
        }}
      />
    </div>
  );
};

export default GameStats;
