import createEngine from "@projectstorm/react-diagrams";
import { toast } from "react-toastify";
import { Diagrams } from "./DiagramsM";
import { Route, Switch } from "react-router";
import "./styles.css";
import Layout from "./Components/Layout/Layout";
import SideBar from "./Components/Layout/SideBar";
import Navbar from "./Components/Layout/Navbar";
import ToolBar from "./Components/Layout/ToolBar";
import { Provider } from "react-redux";
import { store } from "./store/store";
import StarterPage from "./Pages/StarterPage";

toast.configure();

export default function App() {
  const engine = createEngine({ registerDefaultDeleteItemsAction: false });
  engine.maxNumberPointsPerLink = 0;

  return (
    <Layout>
      <Switch>
        <Route path="/" exact>
          <StarterPage />
        </Route>
        <Route path="/edit" exact>
          <Navbar />
          <div className="content">
            <SideBar />
            <Diagrams engine={engine} />
            <Provider store={store}>
              <ToolBar engine={engine} />
            </Provider>
          </div>
        </Route>
      </Switch>
    </Layout>
  );
}
