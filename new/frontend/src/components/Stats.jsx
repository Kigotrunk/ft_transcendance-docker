import React, { useContext, useEffect, useState } from "react";
import axios from "axios";
import History from "./History";
import Chart from "chart.js/auto";
import { Doughnut, Bar } from "react-chartjs-2";
import "../css/stats.css";
import { AuthContext } from "../AuthContext";
import BarChartIcon from "@mui/icons-material/BarChart";
import DonutLargeIcon from "@mui/icons-material/DonutLarge";
import { useTranslation } from "react-i18next";

const Stats = () => {
    const { t } = useTranslation();
  const { user } = useContext(AuthContext);
  const [profile, setProfile] = useState({});
  const [pieSelected, setPieSelected] = useState(false);

  const getProfile = async () => {
    try {
      const response = await axios.get(
        `https://localhost:8000/api/profile/${user.id}/`
      );
      console.log(response.data);
      setProfile(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    getProfile();
  }, []);

  return (
    <div className="stats-content">
      <h2>{t('Stats')}</h2>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          gap: "80px",
          width: "90%",
          flexWrap: "wrap",
          justifyContent: "center",
        }}
      >
        <div className="stats-block">
          <span className="stats-label">{t('Best Survival Score')}</span>
          <p>{profile.highest_score}</p>
        </div>
        <div className="stats-block">
          <span className="stats-label">{t('Points')}</span>
          <p>{profile.elo}</p>
        </div>
        <div className="stats-block">
          <span className="stats-label">{t('Wins')}</span>
          <p>{profile.nb_win}</p>
        </div>
        <div className="stats-block">
          <span className="stats-label">{t('Defeats')}</span>
          <p>{profile.nb_loose}</p>
        </div>
        <div className="stats-block">
          <span className="stats-label">Top 8</span>
          <p>{profile.nb_top8}</p>
        </div>
        <div className="stats-block">
          <span className="stats-label">Top 4</span>
          <p>{profile.nb_top4}</p>
        </div>
        <div className="stats-block">
          <span className="stats-label">Top 2</span>
          <p>{profile.nb_top2}</p>
        </div>
        <div className="stats-block">
          <span className="stats-label">Top 1</span>
          <p>{profile.nb_top1}</p>
        </div>
      </div>
      <div
        style={{
          position: "relative",
          display: "flex",
          flexDirection: "row",
          gap: "80px",
          width: "90%",
          flexWrap: "wrap",
          justifyContent: "center",
        }}
      >
        <button
          className="chart-button"
          onClick={() => setPieSelected((prev) => !prev)}
          style={{
            height: "50px",
            width: "50px",
            position: "absolute",
            top: "50px",
            left: "0",
          }}
        >
          {pieSelected ? <BarChartIcon /> : <DonutLargeIcon />}
        </button>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <h3>{t('Wins')} / {t('Defeats')}</h3>
          <div style={{ height: "360px" }}>
            {pieSelected ? (
              <Doughnut
                data={{
                  labels: ["Wins", "Defeats"],
                  datasets: [
                    {
                      data: [profile.nb_win, profile.nb_loose],
                      backgroundColor: [
                        "rgba(0, 255, 0, 0.6)",
                        "rgba(255, 0, 0, 0.6)",
                      ],
                      borderWidth: 0,
                      hoverOffset: 10,
                    },
                  ],
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      display: false,
                    },
                  },
                  layout: {
                    padding: 10,
                  },
                }}
                width={"320px"}
                height={"320px"}
              />
            ) : (
              <Bar
                data={{
                  labels: ["wins", "defeats"],
                  datasets: [
                    {
                      label: "Wins / Defeats",
                      data: [profile.nb_win, profile.nb_loose],
                      backgroundColor: [
                        "rgba(0, 255, 0, 0.6)",
                        "rgba(255, 0, 0, 0.6)",
                      ],
                    },
                  ],
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                    y: {
                      beginAtZero: true,
                    },
                  },
                  plugins: {
                    legend: {
                      display: false,
                    },
                  },
                }}
              />
            )}
          </div>
        </div>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <h3>{t('Cup Results')}</h3>
          <div style={{ height: "360px" }}>
            {pieSelected ? (
              <Doughnut
                data={{
                  labels: ["Top 8", "Top 4", "Top 2", "Top 1"],
                  datasets: [
                    {
                      data: [
                        profile.nb_top8,
                        profile.nb_top4,
                        profile.nb_top2,
                        profile.nb_top1,
                      ],
                      backgroundColor: [
                        "#36A2EB",
                        "#FF6384",
                        "#4BC0C0",
                        "#FFCE56",
                      ],
                      borderWidth: 0,
                      hoverOffset: 10,
                    },
                  ],
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      display: false,
                    },
                  },
                  layout: {
                    padding: 10,
                  },
                }}
                width={"320px"}
                height={"320px"}
              />
            ) : (
              <Bar
                data={{
                  labels: ["Top 8", "Top 4", "Top 2", "Top 1"],
                  datasets: [
                    {
                      data: [
                        profile.nb_top8,
                        profile.nb_top4,
                        profile.nb_top2,
                        profile.nb_top1,
                      ],
                      backgroundColor: [
                        "#36A2EB",
                        "#FF6384",
                        "#4BC0C0",
                        "#FFCE56",
                      ],
                      borderWidth: 0,
                      hoverOffset: 10,
                    },
                  ],
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                    y: {
                      beginAtZero: true,
                    },
                  },
                  plugins: {
                    legend: {
                      display: false,
                    },
                  },
                }}
              />
            )}
          </div>
        </div>
      </div>
      <h2>{t('History')}</h2>
      <History id={user.id} />
    </div>
  );
};

export default Stats;
