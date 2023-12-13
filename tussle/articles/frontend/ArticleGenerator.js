import React, {useEffect, useCallback} from 'react';
import "./ArticleGenerator.scss";
import {api} from "../../general/frontend/components/api";
import CircularProgress from "@mui/material/CircularProgress";
import {generateArticlePrompt} from "./ArticleGeneration";
import {ArticleSectionDisplay} from "./ArticleSectionDisplay";

let globalIsGenerating = false;

export default function ArticleGenerator({article, answer}) {
    const [sections, setSections] = React.useState([]);
    const [remainingPrompts, setRemainingPrompts] = React.useState(article.prompts);

    const addNextSectionGeneratedText = useCallback((nextSectionPrompt, generatedText) => {
        const newSections = sections.slice();
        newSections.push({
            ...nextSectionPrompt,
            generated: generatedText,
        });
        setSections(newSections);
        setRemainingPrompts(remainingPrompts.slice(1));
    }, [sections, setSections, remainingPrompts, setRemainingPrompts]);

    const executeOneCompletion = useCallback(() => {
        globalIsGenerating = true;
        return new Promise((resolve, reject) => {
            const nextSectionPrompt = remainingPrompts[0];
            if (nextSectionPrompt.disable_ai) {
                setTimeout(() => {
                    globalIsGenerating = false;
                    addNextSectionGeneratedText(nextSectionPrompt, nextSectionPrompt.text);
                    resolve();
                }, 500);
            } else {
                const nextSectionPromptText = nextSectionPrompt.text;
                const prompt = generateArticlePrompt(article.paragraph_generating_prompt, sections, answer, nextSectionPromptText);
                api.getCompletion(prompt).then((response) => {
                    globalIsGenerating = false;
                    addNextSectionGeneratedText(nextSectionPrompt, response.completion);
                    resolve();
                }).catch((error) => {
                    globalIsGenerating = false;
                    reject(error);
                });
            }
        });
    }, [remainingPrompts, sections, addNextSectionGeneratedText, answer, article]);

    useEffect(() => {
        if (!globalIsGenerating && remainingPrompts.length > 0) {
            executeOneCompletion().then(() => {
                // Do nothing
            }).catch((error) => {
                // Do nothing
            });
        }
    }, [remainingPrompts, executeOneCompletion]);

    return (
        <>
            {
                sections.map((section, sectionIndex) => {
                    return <ArticleSectionDisplay prompt={section} key={sectionIndex}/>
                })
            }
            {
                remainingPrompts.length > 0 ?
                    <div className={"spinner-wrapper"}>
                        <CircularProgress/>
                    </div>
                    : null
            }
        </>
    );
}