import Button from "@mui/material/Button";
import {useState} from "react";
import CircularProgress from "@mui/material/CircularProgress";
import React from "react";
import "./SpinnerButton.scss";

export function SpinnerButton(props) {
    const [isSpinnerShowing, setIsSpinnerShowing] = useState(false);
    const spinnerColor = props.spinnerColor || "primary";

    const handleOnClick = (evt) => {
        if (props.onClick) {
            if (isSpinnerShowing) {
                // Don't allow clicking the button again if its already showing a spinner,
                // this prevents double clicking.
                return;
            }

            setIsSpinnerShowing(true);

            try {
                const promise = props.onClick(evt);
                if (!promise) {
                    setIsSpinnerShowing(false);
                    return;
                }

                promise.then((result) => {
                    setIsSpinnerShowing(false);
                    return result;
                }).catch(err => {
                    setIsSpinnerShowing(false)
                    return err;
                });
            } catch(err) {
                setIsSpinnerShowing(false);
                throw err;
            }
        }
    };

    const className = `${props.className || ""} spinner-button`.trim();

    const newProps = {
        ...props,
        className: className,
        onClick: handleOnClick,
        startIcon: isSpinnerShowing ? null : props.startIcon,
        endIcon: isSpinnerShowing ? null : props.endIcon,
    }

    return <Button {...newProps}>
        {
            isSpinnerShowing ?
                <CircularProgress size={24} color={spinnerColor} />
                : props.children
        }
    < /Button>
}

