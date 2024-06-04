import React from "react";
import { Route, Routes } from "react-router-dom";
import Chat from "./components/Chat";
import Pong from "./components/Pong";
import Home from "./components/Home";
import PrivateLayout from "./PrivateLayout";

const PrivateRouter = () => {
  return (
    <Routes>
      <Route element={<PrivateLayout />}>
        <Route path="/home" element={<Home />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/pong" element={<Pong />} />
      </Route>
    </Routes>
  );
};

export default PrivateRouter;
