import React from 'react';
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import FadeInOut from './FadeInOut';
import "./Explainer.scss";
import CircularProgress from '@mui/material/CircularProgress';
import "./GeneratingArticlePlaceholder.scss";

export default function GeneratingArticlePlaceholder({text, showAfterMs, hideAfterMs}) {
    return (
        <FadeInOut showAfterMs={showAfterMs} hideAfterMs={hideAfterMs}>
            <div className="generating-article-placeholder">
                <Card className="generating-article-placeholder-card">
                    <CardContent>
                        <Typography variant="h6" component="div">
                            Your article is currently generating.....
                        </Typography>
                        <CircularProgress />
                    </CardContent>
                </Card>
            </div>
        </FadeInOut>
    );
}