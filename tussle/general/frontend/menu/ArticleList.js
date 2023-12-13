import React, { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import AddIcon from '@mui/icons-material/Add';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import {api} from "../components/api";
import {ArticleListItem} from "./ArticleListItem";
import "./ArticleList.scss";
import CircularProgress from "@mui/material/CircularProgress";

export function ArticleList() {
    const { isAuthenticated } = useAuth0();
    const [articles, setArticles] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (process.env.REACT_APP_USE_GCP_STORAGE_ARTICLE_CACHE === "true") {
            setIsLoading(true);
            api.getArticlesFromGCPStorageCache().then((data) => {
                setArticles(data);
                setIsLoading(false);

                // We still fetch the debate from the underlying API server as well, just in case
                // cache is stale (and it also forces the server to wake up if needed)
                api.getArticles().then((data) => {
                    setArticles(data);
                });
            }, (err) => {
                // GCP storage failed. Situation must be pretty bad. So lets try fetching
                // from the API server instead.
                api.getArticles().then((data) => {
                    setArticles(data);
                    setIsLoading(false);
                }, (err) => {
                    setIsLoading(false);
                });
            });
        } else {
            // Just get directly from the API server, and bypass the gcp storage article cache
            setIsLoading(true);
            api.getArticles().then((data) => {
                setArticles(data);
                setIsLoading(false);
            }, (err) => {
                setIsLoading(false);
            });
        }
    }, []);

    function onCreateNewArticleClicked(evt) {
        evt.stopPropagation();

        api.createNewArticle().then((article) => {
            setArticles([...articles, article]);
        });
    }

    return <List className={"article-list"}>
        {articles.map((article) =>
            <ArticleListItem key={article._id} article={article} />
        )}
        {
            isLoading ? <CircularProgress /> : null
        }
        {
            isAuthenticated ?
                <ListItem disablePadding className={"create-article-item"}>
                    <Button
                        className={"create-new-article-button"}
                        onClick={onCreateNewArticleClicked}
                        variant={"contained"}
                        color={"primary"}
                        endIcon={<AddIcon />
                        }>New Article</Button>
                </ListItem>
                : null
        }
    </List>;
}