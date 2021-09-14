import createEngine from "@projectstorm/react-diagrams";
import * as React from "react";
import { Menu } from "./Components/UI/Menu-UI/Menu";
import { Diagrams } from "./DiagramsM";
import "./styles.css";
import Layout from "./Components/Layout/Layout";
import SideBar from "./Components/Layout/SideBar";
import Navbar from "./Components/Layout/Navbar";
import ToolBar from "./Components/Layout/ToolBar";

const engine = createEngine();

export default function App() {
  return (
    <Layout>
      <Navbar />
      <div className="content">
        <SideBar />
        <div className="App">
          <Diagrams engine={engine} />
        </div>
        <ToolBar engine={engine} />
      </div>
    </Layout>
  );
}
