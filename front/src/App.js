import React from "react";
import { Routes, Route } from "react-router-dom";
import SongTable from "./components/SongTable";
import Discovery from "./pages/Discovery";


function App() {
  return (
    <div className="fullPageContainer" fluid>
      <Routes>
        <Route path="/" element={<SongTable />} />
        <Route path="/discovery" element={<Discovery />} />
      </Routes>
    </div>
  )};

  export default App