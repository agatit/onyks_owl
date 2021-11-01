import { toast } from "react-toastify";
import { Route, Switch } from "react-router";
import "./styles.css";
import Layout from "./Components/Layout/Layout";
import { Provider } from "react-redux";
import store from "./store/store";
import { Provider as ReduxQueryProvider } from "redux-query-react";
import StarterPage from "./Pages/StarterPage";
import PlayerPage from "./Pages/PlayerPage";
import EditorPage from "./Pages/EditorPage";
import Navbar from "./Components/Layout/Navbar";

toast.configure();

export const getQueries = (state: any) => state.queries;

export default function App() {
  return (
    <Layout>
      <Switch>
        <Provider store={store}>
          <ReduxQueryProvider queriesSelector={getQueries}>
            <Route path="/" exact>
              <StarterPage />
            </Route>
            <Route path="/player/:projectID" exact>
              <PlayerPage />
            </Route>
            <Route path="/edit/:projectID" exact>
              <Navbar />
              <EditorPage />
            </Route>
          </ReduxQueryProvider>
        </Provider>
      </Switch>
    </Layout>
  );
}
