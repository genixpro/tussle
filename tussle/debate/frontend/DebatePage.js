import "./DebatePage.scss";
import {useCallback, useEffect, useState} from "react";
import {SpinnerButton} from "../../general/frontend/components/SpinnerButton";

export function DebatePage(props) {
    const [isReady, setIsReady] = useState(false);
    const [topic, setTopic] = useState(null);

    const handleReadyClicked = useCallback(() => {
        setIsReady(true);
    }, [setIsReady]);

    return <div className={"debate-page"}>
        <h1>Get ready to debate!</h1>
        <p>You will be given a topic and a position.</p>
        <p>You have three minutes to construct an argument in favor of your position.</p>

        <SpinnerButton
            variant="contained"
            color="primary"
            className={"go-button"}
            onClick={handleReadyClicked}
        >
            I'm Ready!
        </SpinnerButton>
    </div>
}
