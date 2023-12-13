import React, {useState, useEffect} from 'react';
import "./FadeInOut.scss";

export default function FadeInOut({children, showAfterMs, hideAfterMs, onHide}) {
    const [isContentVisible, setIsContentVisible] = useState(false);
    const [isFadingIn, setIsFadingIn] = useState(false);
    const [isFadingOut, setIsFadingOut] = useState(false);
    const fadeTime = 300;

    useEffect(() => {
        setTimeout(() => {
            setIsContentVisible(true);
            setIsFadingIn(true);
        }, showAfterMs);

        if (hideAfterMs) {
            setTimeout(() => {
                setIsFadingOut(true);
            }, showAfterMs + hideAfterMs - fadeTime);

            setTimeout(() => {
                setIsFadingOut(true);
                setIsContentVisible(false);
                if (onHide) {
                    onHide();
                }
            }, showAfterMs + hideAfterMs);
        }
    }, [onHide, showAfterMs, hideAfterMs]);

    if (!isContentVisible) {
        return <></>;
    }

    const isVisibleState = !isFadingIn && !isFadingOut;

    const contentClass = `fade-in-out ${isFadingIn ? "fade-in" : ""} ${isFadingOut ? "fade-out" : ""} ${isVisibleState ? "visible" : ""}`

    return (
        <div className={contentClass}>
            {children}
        </div>
    );
}