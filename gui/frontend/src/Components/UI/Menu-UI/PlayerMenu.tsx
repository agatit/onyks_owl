import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlay, faPause, faExpand } from "@fortawesome/free-solid-svg-icons";
import classes from "./PlayerMenu.module.css";
import { useState } from "react";
import { engineActionTypes } from "../../../store/Reducers/engineReducer";
import { connect } from "react-redux";

interface PlayerMenuProps {
  zoomToFit: () => any;
}

function PlayerMenu(props: PlayerMenuProps) {
  const [isPlaying, setPlayingState] = useState(false);

  function togglePlayingState() {
    setPlayingState(!isPlaying);
  }

  return (
    <div className={classes.PlayerMenu}>
      <div className={classes.controls}>
        <span>
          <FontAwesomeIcon
            icon={faExpand}
            color="white"
            size="lg"
            onClick={props.zoomToFit}
          />
        </span>
        <span onClick={togglePlayingState} className={classes.playBtn}>
          {isPlaying ? (
            <FontAwesomeIcon icon={faPause} color="grey" size="2x" />
          ) : (
            <FontAwesomeIcon icon={faPlay} color="green" size="2x" />
          )}
        </span>
      </div>
    </div>
  );
}

const mapDispatchToProps = (dispatch: any, ownProps: any) => ({
  zoomToFit: () => dispatch({ type: engineActionTypes.ZOOM_TO_FIT }),
});

export default connect(null, mapDispatchToProps)(PlayerMenu);
