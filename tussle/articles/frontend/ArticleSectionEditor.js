import React from 'react';
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import TextField from "@mui/material/TextField";
import "./ArticleSectionEditor.scss";
import CircularProgress from "@mui/material/CircularProgress";
import {ArticleSectionDisplay} from "./ArticleSectionDisplay";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";

export function ArticleSectionEditor({prompt, onChange, onChangeHeading, onChangeDisableAI, regenerateTextForPrompt}) {
    const [tabValue, setTabValue] = React.useState(1);
    const [isRegenerating, setIsRegenerating] = React.useState(false);

    const handleTabChanged = (event, nextTab) => {
        if ((nextTab === 1 || nextTab === 2) && nextTab !== tabValue) {
            setIsRegenerating(true);
            regenerateTextForPrompt().then(() => {
                setIsRegenerating(false);
            }).catch((error) => {
                setIsRegenerating(false);
            });
        }

        setTabValue(nextTab);
    }


    function handleOnChange(evt) {
        onChange(evt.target.value);
    }

    function handleOnHeadingChange(evt) {
        onChangeHeading(evt.target.value);
    }

    function handleDisableAIChanged(evt) {
        onChangeDisableAI(evt.target.checked);
    }

    return (
        <div className="article-section-editor">
            <Card className="article-section-editor-card">
                <CardContent>
                    <Tabs value={tabValue} onChange={handleTabChanged} aria-label="Article Editor">
                        <Tab label="Edit Section"/>
                        <Tab label="View Generated Text"/>
                        <Tab label="View Prompt"/>
                    </Tabs>
                    {
                        tabValue === 0 ?
                            <>
                                <TextField
                                    label="Optional Section Heading"
                                    maxRows={1}
                                    value={prompt.heading}
                                    onChange={handleOnHeadingChange}
                                />
                                <TextField
                                    label="Section Text"
                                    multiline
                                    maxRows={12}
                                    value={prompt.text}
                                    onChange={handleOnChange}
                                />
                                <FormControlLabel
                                    value={prompt.disable_ai}
                                    control={
                                        <Checkbox
                                            checked={prompt?.disable_ai}
                                            onChange={handleDisableAIChanged}
                                        />
                                    }
                                    label="Disable AI"
                                />
                            </>: null
                    }
                    {
                        tabValue === 1 && isRegenerating ?
                            <CircularProgress />
                            : null
                    }
                    {
                        tabValue === 1 && !isRegenerating ?
                            <ArticleSectionDisplay prompt={prompt}/>
                            : null
                    }
                    {
                        tabValue === 2 ?
                            <p className={"filled-prompt"}>{prompt.filled_prompt}</p>
                            : null
                    }
                </CardContent>
            </Card>
        </div>
    );
}