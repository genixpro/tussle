import React from "react";
import {computeDocumentTitle} from "./ArticleView";

export function ArticleMetaTags({article}) {
    return <>
        <meta name="description"
              content={`${article.title} - A self-customizing article written by Bradley Arsenault on Tussle.`}/>
        <meta property="og:title" content={computeDocumentTitle(article)}/>
        <meta property="og:image" content="/logo1024.jpg" />
        <meta property="og:type" content="article"/>
        <meta property="og:url" content={`https://tussle.bradleyarsenault.me/article/${article.slug}`}/>
    </>;
}