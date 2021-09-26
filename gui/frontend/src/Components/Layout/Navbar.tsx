import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlay, faPause, faCog } from "@fortawesome/free-solid-svg-icons";

import classes from "./Navbar.module.css";
import { Link } from "react-router-dom";

function Navbar(props: any) {
  return (
    <header className={classes.navbar}>
      <Link to="/" style={{ textDecoration: "none" }}>
        <div className={classes.logo}> Onyks_owl</div>
      </Link>
      <div className={classes.controls}>
        <FontAwesomeIcon icon={faPlay} color="green" size="2x" />
        <FontAwesomeIcon icon={faPause} color="grey" size="2x" />
      </div>
      <FontAwesomeIcon icon={faCog} color="grey" size="2x" />
    </header>
  );
}

export default Navbar;
