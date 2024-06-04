import React from "react";
import "./css/colors.css";
import "./css/index.css";
import { AuthProvider } from "./AuthContext";
import PublicRouter from "./PublicRouter";
import PrivateRouter from "./PrivateRouter";
import { BrowserRouter } from "react-router-dom";

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <PublicRouter />
        <PrivateRouter />
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
