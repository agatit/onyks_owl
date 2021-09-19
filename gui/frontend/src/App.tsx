import createEngine from "@projectstorm/react-diagrams";
import * as React from "react";
import { toast } from "react-toastify";
import { Diagrams } from "./DiagramsM";
import "./styles.css";
import Layout from "./Components/Layout/Layout";
import SideBar from "./Components/Layout/SideBar";
import Navbar from "./Components/Layout/Navbar";
import ToolBar from "./Components/Layout/ToolBar";
import { connect, Provider } from "react-redux";
import { store } from "./store/store";
import { selectedNode } from "./store/Actions/nodeActions";

toast.configure();

export default function App() {
  const engine = createEngine();

  return (
    <Provider store={store}>
      <Layout>
        <Navbar />
        <div className="content">
          <SideBar />
          <Diagrams engine={engine} />
          <ToolBar engine={engine} />
        </div>
      </Layout>
    </Provider>
  );
}
