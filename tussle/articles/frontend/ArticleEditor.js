import "./ArticleEditor.scss";
import Button from "@mui/material/Button";
import React, {useCallback, useEffect, useMemo} from 'react';
import debounce from "lodash/debounce";
import {ArticleSectionEditor} from "./ArticleSectionEditor";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import TextField from "@mui/material/TextField";
import {api} from "../../general/frontend/components/api";
import {generateArticlePrompt} from "./ArticleGeneration";
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import {ArticleView} from "./ArticleView";


function ArticleBasicInfoEditor({article, changeArticle}) {
    const handleTitleChanged = (newTitle) => {
        const newArticle = {
            ...article,
            title: newTitle,
        };
        changeArticle(newArticle);
    }

    const handleSlugChanged = (newSlug) => {
        const newArticle = {
            ...article,
            slug: newSlug,
        };
        changeArticle(newArticle);
    }

    const handleQuestionChanged = (newQuestion) => {
        const newArticle = {
            ...article,
            question: newQuestion,
        };
        changeArticle(newArticle);
    }

    const handleQuestionPlaceholderChanged = (newQuestionPlaceholder) => {
        const newArticle = {
            ...article,
            question_placeholder: newQuestionPlaceholder,
        };
        changeArticle(newArticle);
    }

    const handleDefaultQuestionAnswerChanged = (newDefaultQuestionAnswer) => {
        const newArticle = {
            ...article,
            default_question_answer: newDefaultQuestionAnswer,
        };
        changeArticle(newArticle);
    };

    const handleDateChange = (newDate) => {
        const newArticle = {
            ...article,
            date: newDate,
        };
        changeArticle(newArticle);
    }

    const handlePublishedChanged = (newPublished) => {
        const newArticle = {
            ...article,
            published: newPublished,
        };
        changeArticle(newArticle);
    }

    return <div className="article-basic-info-editor">
        <Card className="article-basic-info-editor-card">
            <CardContent>
                <p>Basic Info for Article</p>
                <TextField
                    variant="outlined"
                    label={"Title"}
                    value={article?.title}
                    onChange={(evt) => handleTitleChanged(evt.target.value)}
                    placeholder={"title..."}
                />
                <TextField
                    variant="outlined"
                    label={"Slug / URL"}
                    value={article?.slug}
                    onChange={(evt) => handleSlugChanged(evt.target.value)}
                    placeholder={"Slug (url / page name)"}
                />
                <TextField
                    variant="outlined"
                    label={"Question"}
                    value={article?.question}
                    onChange={(evt) => handleQuestionChanged(evt.target.value)}
                    placeholder={"Question to ask user"}
                />
                <TextField
                    variant="outlined"
                    label={"Question Placeholder"}
                    value={article?.question_placeholder}
                    onChange={(evt) => handleQuestionPlaceholderChanged(evt.target.value)}
                    placeholder={"Placeholder for input box on question to ask user. Use something like 'Enter your answer here...' but customized"}
                />
                <TextField
                    variant="outlined"
                    label={"Default Question Answer"}
                    value={article?.default_question_answer}
                    onChange={(evt) => handleDefaultQuestionAnswerChanged(evt.target.value)}
                    placeholder={"Default answer to question. Used for people who don't have their own answer."}
                />
                <TextField
                    variant="outlined"
                    label={"Date"}
                    value={article?.date}
                    onChange={(evt) => handleDateChange(evt.target.value)}
                    placeholder={"Date of article. Use format 'MONTH DAY, YEAR'"}
                />
                <FormControlLabel
                    value={article?.published}
                    control={
                        <Checkbox
                            checked={article?.published}
                            onChange={(evt) => handlePublishedChanged(evt.target.checked)}
                        />
                    }
                    label="Published"
                />
            </CardContent>
        </Card>
    </div>;
}

function TestingAnswerEditor({testingQuestionAnswer, setTestingQuestionAnswer, article}) {
    return (
        <div className="article-testing-answer-editor">
            <Card className="article-testing-answer-editor-card">
                <CardContent>
                    <p>Please put in the question-answer you want to use when testing article generation.</p>
                    <TextField
                        multiline
                        label={"Testing Answer"}
                        rows={4}
                        variant="outlined"
                        value={testingQuestionAnswer}
                        onChange={(evt) => setTestingQuestionAnswer(evt.target.value)}
                        placeholder={article.question}
                    />
                </CardContent>
            </Card>
        </div>
    );
}

function ArticleGeneratingPromptEditor({article, changeArticle}) {
    const handleParagraphGeneratingPromptChanged = (newParagraphGeneratingPrompt) => {
        const newArticle = {
            ...article,
            paragraph_generating_prompt: newParagraphGeneratingPrompt,
        };
        changeArticle(newArticle);
    };


    return (
        <div className="article-generating-prompt-editor">
            <Card className="article-generating-prompt-editor-card">
                <CardContent>
                    <p>
                        This allows you to edit the prompt that is used for generating each paragraph in the article.
                        <br/>
                        <br/>
                        There are three insertion points in the generating prompt, that will be substituted with real values.
                        <br/>
                        <br/>
                        Those are "<strong>$answer</strong>" for the users answer to the question. "<strong>$existing</strong>" for all of the existing article sections
                        that have already been written. And "<strong>$next</strong>" for the next paragraph section to be written.
                    </p>

                    <TextField
                        multiline
                        label={"Generating Prompt"}
                        rows={12}
                        variant="outlined"
                        value={article.paragraph_generating_prompt}
                        onChange={(evt) => handleParagraphGeneratingPromptChanged(evt.target.value)}
                        placeholder={"Generating Prompt"}
                    />
                </CardContent>
            </Card>
        </div>
    );
}

export function ArticleContentEditor({article, changeArticle}) {
    const [testingQuestionAnswer, setTestingQuestionAnswer] = React.useState("A mobile app that identifies the breed of dogs by photo.");

    const regenerateTextForPrompt = useCallback((promptToRegenerate) => {
        // Put together all the generated sections leading up to the current prompt
        const generatedSections = article.prompts.slice(0, article.prompts.indexOf(promptToRegenerate)).map((prompt) => {
            return prompt.generated;
        });

        function handleGeneratedText(generatedPrompt, generatedText) {
            const modifiedPrompts = article.prompts.map((existingPrompt) => {
                if (existingPrompt.id === promptToRegenerate.id) {
                    return {
                        ...promptToRegenerate,
                        filled_prompt: generatedPrompt,
                        generated: generatedText,
                    }
                } else {
                    return existingPrompt;
                }
            });

            const newArticle = {
                ...article,
                prompts: modifiedPrompts,
            };

            changeArticle(newArticle);
        }

        if (promptToRegenerate.disable_ai) {
            handleGeneratedText(promptToRegenerate.text, promptToRegenerate.text);
            return Promise.resolve();
        } else {
            const generatedPrompt = generateArticlePrompt(article.paragraph_generating_prompt, generatedSections, testingQuestionAnswer, promptToRegenerate.text);
            return api.getCompletion(generatedPrompt).then((response) => {
                handleGeneratedText(generatedPrompt, response.completion);
            });
        }
    }, [article, changeArticle, testingQuestionAnswer]);

    const handleAddPromptClicked = () => {
        const newPrompt = {
            id: `${Math.random().toString().substring(3)}`,
            text: "Please enter text for your new section...",
            generated: ""
        };
        const newArticle = {
            ...article,
            prompts: [
                ...article.prompts,
                newPrompt,
            ]
        }

        changeArticle(newArticle);
    };

    const handlePromptTextChanged = (promptId, newPromptText) => {
        const modifiedPrompts = article.prompts.map((prompt) => {
            if (prompt.id === promptId) {
                return {
                    ...prompt,
                    text: newPromptText,
                }
            } else {
                return prompt;
            }
        });

        const newArticle = {
            ...article,
            prompts: modifiedPrompts,
        };

        changeArticle(newArticle);
    }

    const handleHeadingTextChanged = (promptId, newHeading) => {
        const modifiedPrompts = article.prompts.map((prompt) => {
            if (prompt.id === promptId) {
                return {
                    ...prompt,
                    heading: newHeading,
                }
            } else {
                return prompt;
            }
        });

        const newArticle = {
            ...article,
            prompts: modifiedPrompts,
        };

        changeArticle(newArticle);
    }

    const handleDisableAIChanged = (promptId, newDisableAISetting) => {
        const modifiedPrompts = article.prompts.map((prompt) => {
            if (prompt.id === promptId) {
                return {
                    ...prompt,
                    disable_ai: newDisableAISetting,
                }
            } else {
                return prompt;
            }
        });

        const newArticle = {
            ...article,
            prompts: modifiedPrompts,
        };

        changeArticle(newArticle);
    }

    if (!article) {
        return null;
    }

    return <div className={"article-content-editor"}>
        <TestingAnswerEditor
            testingQuestionAnswer={testingQuestionAnswer}
            setTestingQuestionAnswer={setTestingQuestionAnswer}
            article={article}
        />
        {
            article && article.prompts.map((prompt, index) => {
                return <ArticleSectionEditor
                    key={prompt.id}
                    prompt={prompt}
                    onChange={(newPromptText) => handlePromptTextChanged(prompt.id, newPromptText)}
                    onChangeHeading={(newHeadingText) => handleHeadingTextChanged(prompt.id, newHeadingText)}
                    onChangeDisableAI={(newHeadingText) => handleDisableAIChanged(prompt.id, newHeadingText)}
                    regenerateTextForPrompt={() => regenerateTextForPrompt(prompt)}
                />
            })
        }
        {
            <div>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleAddPromptClicked}
                >
                    Add Section
                </Button>
            </div>
        }
    </div>
}


export function ArticleEditor(props) {
    const [article, setArticle] = React.useState(null);
    const [tabValue, setTabValue] = React.useState(0);

    useEffect(() => {
        if (props.articleId) {
            api.getArticle(props.articleId).then((article) => {
                setArticle(article);
            });
        }
    }, [props.articleId]);

    const saveArticle = useCallback((article) => {
        api.saveArticle(article);
    }, []);

    const saveArticleDebounced = useMemo(
        () => debounce(saveArticle, 500),
        [saveArticle]
    );

    const onArticleChanged = (newArticle) => {
        setArticle(newArticle);
        saveArticleDebounced(newArticle);
    }

    const handleTabChanged = (event, newValue) => {
        setTabValue(newValue);
    };

    if (!article) {
        return null;
    }

    return <div className={"article-editor"}>
        <Card className="article-tabs-card">
            <Tabs value={tabValue} onChange={handleTabChanged} aria-label="Article Editor">
                <Tab label="Basic Settings"/>
                <Tab label="Generating Prompt"/>
                <Tab label="Edit Content"/>
                <Tab label="View"/>
            </Tabs>
        </Card>
        {
            tabValue === 0 ?
                <>
                    <ArticleBasicInfoEditor
                        article={article}
                        changeArticle={onArticleChanged}
                    />
                </>
            : null
        }
        {
            tabValue === 1 ?
                <>
                    <ArticleGeneratingPromptEditor
                        article={article}
                        changeArticle={onArticleChanged}
                    />
                </>
            : null
        }
        {
            tabValue === 2 ?
                <>
                    <ArticleContentEditor
                        article={article}
                        changeArticle={onArticleChanged}
                    />
                </>
            : null
        }
        {
            tabValue === 3 ?
                <>
                    <ArticleView articleId={article._id}/>
                </>
            : null
        }
    </div>;
}

