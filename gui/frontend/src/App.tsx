import createEngine from "@projectstorm/react-diagrams";
import * as React from "react";
import { Menu } from "./Components/UI/Menu-UI/Menu";
import { Diagrams } from "./DiagramsM";
import "./styles.css";
import Layout from "./Components/Layout/Layout";
import SideBar from "./Components/Layout/SideBar";
import Navbar from "./Components/Layout/Navbar";
import ToolBar from "./Components/Layout/ToolBar";

export default function App() {
  const engine = createEngine();

  return (
    <Layout>
      <Navbar />
      <div className="content">
        <SideBar />

        <Diagrams engine={engine} />

        <ToolBar engine={engine} />
      </div>
    </Layout>
  );
}
