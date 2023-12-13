import React from "react";
import "./ArticleSectionDisplay.scss";


export function ArticleSectionDisplay({prompt}) {
    return <div className={"article-section-display"}>
        {prompt.heading ? <h2>{prompt.heading}</h2> : null}
        <p>{prompt.generated}</p>
    </div>
}