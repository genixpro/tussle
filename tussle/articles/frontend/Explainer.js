import React from 'react';
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import FadeInOut from './FadeInOut';
import "./Explainer.scss";

export default function Explainer({text, showAfterMs, hideAfterMs, onHide}) {
    return (
        <FadeInOut
            showAfterMs={showAfterMs}
            hideAfterMs={hideAfterMs}
            onHide={onHide}
        >
            <div className="explainer">
                <Card className="explainer-card">
                    <CardContent>
                        <Typography variant="h6" component="div">
                            {text}
                        </Typography>
                        <div>
                            <Typography variant="body2" className={"skip-text"}>
                                Click to skip.
                            </Typography>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </FadeInOut>
    );
}