import React from "react";
import { Routes, Route } from "react-router-dom";
import Accueil from "./components/Accueil";
import Login from "./components/Login";
import Register from "./components/Register";

const PublicRouter = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/" element={<Accueil />} />
    </Routes>
  );
};

export default PublicRouter;
