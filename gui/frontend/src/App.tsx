import { toast } from "react-toastify";
import Diagrams from "./DiagramsM";
import { Route, Switch } from "react-router";
import "./styles.css";
import Layout from "./Components/Layout/Layout";
import SideBar from "./Components/Layout/SideBar";
import Navbar from "./Components/Layout/Navbar";
import ToolBar from "./Components/Layout/ToolBar";
import { Provider } from "react-redux";
import { store } from "./store/store";
import StarterPage from "./Pages/StarterPage";
import PlayerMenu from "./Components/UI/Menu-UI/PlayerMenu";
import PlayerPage from "./Pages/PlayerPage";

toast.configure();

export default function App() {
  return (
    <Layout>
      <Switch>
        <Provider store={store}>
          <Route path="/" exact>
            <StarterPage />
          </Route>
          <Route path="/player" exact>
            <PlayerPage />
          </Route>
          <Route path="/edit" exact>
            <Navbar />
            <div className="content">
              <SideBar />
              <Diagrams />

              <ToolBar />
            </div>
          </Route>
        </Provider>
      </Switch>
    </Layout>
  );
}
