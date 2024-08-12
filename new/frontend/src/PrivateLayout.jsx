import React, { useContext, useState } from "react";
import { Outlet, Navigate } from "react-router-dom";
import Header from "./components/Header";
import Menu from "./components/Menu";
import { AuthContext } from "./AuthContext";

const PrivateLayout = () => {
  const { isLog, isLoading } = useContext(AuthContext);
  const [showPhoneMenu, setShowPhoneMenu] = useState(false);

  if (isLoading) {
    return <div>Loading...</div>;
  }
  return isLog ? (
    <>
      <Header setShowPhoneMenu={setShowPhoneMenu} />
      <div style={{ display: "flex", flexDirection: "row", flexGrow: 1 }}>
        <Menu
          showPhoneMenu={showPhoneMenu}
          setShowPhoneMenu={setShowPhoneMenu}
        />
        <div className="content" style={{ flexGrow: 1 }}>
          <Outlet />
        </div>
      </div>
    </>
  ) : (
    <Navigate to="/login" />
  );
};

export default PrivateLayout;
