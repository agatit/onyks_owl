import createEngine from "@projectstorm/react-diagrams";

import { toast } from "react-toastify";
import { Diagrams } from "./DiagramsM";
import "./styles.css";
import Layout from "./Components/Layout/Layout";
import SideBar from "./Components/Layout/SideBar";
import Navbar from "./Components/Layout/Navbar";
import ToolBar from "./Components/Layout/ToolBar";
import { Provider } from "react-redux";
import { store } from "./store/store";

toast.configure();

export default function App() {
  const engine = createEngine({ registerDefaultDeleteItemsAction: false });

  return (
    <Layout>
      <Navbar />
      <div className="content">
        <SideBar />
        <Diagrams engine={engine} />
        <Provider store={store}>
          <ToolBar engine={engine} />
        </Provider>
      </div>
    </Layout>
  );
}
