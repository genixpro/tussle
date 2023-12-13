import {useParams} from "react-router-dom";
import {useAuth0} from "@auth0/auth0-react";
import {PageWrapper} from "../app/PageWrapper";
import React from "react";
import {ArticleView} from "../../../articles/frontend/ArticleView";
import {ArticleEditor} from "../../../articles/frontend/ArticleEditor";

export const ViewArticlePage = (props) => {
    const params = useParams();
    const articleId = params.articleId;

    const {isAuthenticated, isLoading} = useAuth0();

    if (isLoading) {
        return null;
    }

    if (!isAuthenticated) {
        return <PageWrapper>
            <ArticleView articleId={articleId} key={articleId} />
        </PageWrapper>;
    } else {
        return <PageWrapper>
            <ArticleEditor articleId={articleId} key={articleId} />
        </PageWrapper>;
    }
}
