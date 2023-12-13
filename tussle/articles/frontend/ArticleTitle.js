import React from 'react';
import "./ArticleTitle.scss";

export default function ArticleTitle({title, subtitle, chapter, article}) {
    return (
        <div className="article-title-widget">
            <h1>
                {title}
            </h1>
        </div>
    );
}