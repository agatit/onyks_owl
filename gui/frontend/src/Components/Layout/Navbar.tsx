import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlay, faPause, faCog } from "@fortawesome/free-solid-svg-icons";
import QueryConfig from "redux-query"; //
import { useRequest } from "redux-query-react"; //
import classes from "./Navbar.module.css";
import { Link } from "react-router-dom";

const myQuery = {
  url: "https://pokeapi.co/api/v2/pokemon/1",
};

function Navbar(props: any) {
  const [state, data] = useRequest(myQuery);

  return (
    <header className={classes.navbar}>
      <Link to="/" style={{ textDecoration: "none" }}>
        <div className={classes.logo}> Onyks_owl</div>
      </Link>
      <FontAwesomeIcon icon={faCog} color="grey" size="2x" />
    </header>
  );
}

export default Navbar;
