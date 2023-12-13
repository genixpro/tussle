import React, {useEffect, useMemo} from 'react';
import "./ArticleView.scss";
import ArticleTitle from "./ArticleTitle";
import {api} from "../../general/frontend/components/api";
import ArticleGenerator from "./ArticleGenerator";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Avatar from "@mui/material/Avatar";
import {ArticleExplainer} from "./ArticleExplainer";
import {ArticleMetaTags} from "./ArticleMetaTags";
import CircularProgress from "@mui/material/CircularProgress";

export function calculateMinutesToRead(article) {
    const wordsPerMinute = 200;
    let numberOfWords = 0;
    for (const prompt of article.prompts) {
        numberOfWords += prompt.generated.split(/[\s\W]+/g).length;
    }
    return Math.ceil(numberOfWords / wordsPerMinute);
}

export function computeDocumentTitle(article) {
    return `${article.title} - ${process.env.REACT_APP_ENVIRONMENT_TITLE}`;
}

export function ArticleView(props) {
    const [article, setArticle] = React.useState(null);
    const [questionAnswer, setQuestionAnswer] = React.useState("");

    useEffect(() => {
        if (props.articleId) {
            if (process.env.REACT_APP_USE_GCP_STORAGE_ARTICLE_CACHE === "true") {
                api.getArticleFromGCPStorageCache(props.articleId).then((article) => {
                    setArticle(article);
                    setQuestionAnswer("");

                    // Set the window title
                    document.title = computeDocumentTitle(article);

                    // Load the article from the API server as well, just in case the cache is stale
                    // This all servers to wake up the API server in-case its in cold-mode
                    api.getArticle(props.articleId).then((article) => {
                        setArticle(article);
                    });
                }).catch((error) => {
                    // Try loading from the API server instead
                    api.getArticle(props.articleId).then((article) => {
                        setArticle(article);
                    });
                });
            } else {
                api.getArticle(props.articleId).then((article) => {
                    setArticle(article);
                    setQuestionAnswer("");

                    // Set the window title
                    document.title = computeDocumentTitle(article);
                });
            }
        }
    }, [props.articleId, setArticle, setQuestionAnswer]);

    const minutesToRead = useMemo(() => {
        if (article) {
            return calculateMinutesToRead(article);
        } else {
            return 0;
        }
    }, [article]);

    if (!article) {
        return <div className={"article-view loading"}>
            <CircularProgress />
        </div>;
    } else if (!questionAnswer) {
        return <ArticleExplainer
            article={article}
            questionAnswer={questionAnswer}
            setQuestionAnswer={setQuestionAnswer}
        />
    } else {
        return <div className={"article-view"}>
            <ArticleMetaTags article={article} />

            <Card>
                <CardContent>

                    <div className={"article-header"}>
                        <Avatar alt="Remy Sharp" src="/profile.jpg"/>
                        <span>Bradley Arsenault</span>
                        <span>-</span>
                        <span>{article.date}</span>
                        <span>-</span>
                        <span>{minutesToRead} minute read</span>
                    </div>

                    <ArticleTitle
                        title={article.title}
                    />

                    <ArticleGenerator
                        article={article}
                        answer={questionAnswer}
                    />

                </CardContent>
            </Card>
            <br/>
            <br/>
        </div>
    }
}

