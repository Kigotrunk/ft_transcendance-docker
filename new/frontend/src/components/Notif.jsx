import React from "react";

const Notif = ({ notifs }) => {
  return (
    <div className="notif-container">
      {notifs.map((notif, index) => (
        <div
          key={index}
          className="global-notif"
          onClick={
            notif.issuer === "tournament_info"
              ? () => {
                  console.log("clicked on game notif");
                }
              : () => {
                  console.log("clicked on chat notif");
                }
          }
        >
          <span>{notif.issuer}</span>
          <span>{notif.message}</span>
        </div>
      ))}
    </div>
  );
};

export default Notif;
