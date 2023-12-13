import React, {useCallback} from "react";
import Explainer from "./Explainer";
import FadeInOut from "./FadeInOut";
import ArticleQuestion from "./ArticleQuestion";
import "./ArticleExplainer.scss";
import {ArticleMetaTags} from "./ArticleMetaTags";

export function ArticleExplainer({article, questionAnswer, setQuestionAnswer}) {
    const [isShowingExplainerOne, setIsShowingExplainerOne] = React.useState(true);
    const [isShowingExplainerTwo, setIsShowingExplainerTwo] = React.useState(false);
    const [isShowingExplainerThree, setIsShowingExplainerThree] = React.useState(false);
    const [isShowingQuestion, setIsShowingQuestion] = React.useState(false);

    const handleHideExplainerOne = useCallback(() => {
        if (isShowingExplainerOne) {
            setIsShowingExplainerOne(false);
            setIsShowingExplainerTwo(true);
        }
    },  [isShowingExplainerOne]);

    const handleHideExplainerTwo = useCallback(() => {
        if (isShowingExplainerTwo) {
            setIsShowingExplainerTwo(false);
            setIsShowingExplainerThree(true);
        }
    }, [isShowingExplainerTwo]);

    const handleHideExplainerThree = useCallback(() => {
        if (isShowingExplainerThree) {
            setIsShowingExplainerThree(false);
            setIsShowingQuestion(true);
        }
    }, [isShowingExplainerThree]);

    const handleSkipExplainers = useCallback(() => {
        setIsShowingExplainerOne(false);
        setIsShowingExplainerTwo(false);
        setIsShowingExplainerThree(false);
        setIsShowingQuestion(true);
    }, []);

    return <div className={"article-explainer"} onClick={handleSkipExplainers}>
        <ArticleMetaTags article={article} />
        {
            isShowingExplainerOne && !isShowingQuestion ?
                <Explainer
                    showAfterMs={0}
                    hideAfterMs={3000}
                    text={"This is a self-customizing article."}
                    onHide={handleHideExplainerOne}
                /> : null
        }
        {
            isShowingExplainerTwo && !isShowingQuestion ?
                <Explainer
                    showAfterMs={0}
                    hideAfterMs={4000}
                    text={"You must answer a question in order to view the article."}
                    onHide={handleHideExplainerTwo}
                /> : null
        }
        {
            isShowingExplainerThree && !isShowingQuestion ?
                <Explainer
                    showAfterMs={0}
                    hideAfterMs={4000}
                    text={"If you do not have an answer, press 'Use Default'."}
                    onHide={handleHideExplainerThree}
                /> : null
        }
        {
            isShowingQuestion ?
                <FadeInOut
                    showAfterMs={0}
                    time={null}
                >
                    <ArticleQuestion
                        article={article}
                        onDone={(answer) => setQuestionAnswer(answer)}
                    />
                </FadeInOut>
                : null
        }
    </div>
}