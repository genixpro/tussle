import "./LeftSideMenu.scss";
import * as React from 'react';
import {ArticleList} from "./ArticleList";


export default function LeftSideMenu() {
    return (
        <div className={"left-side-menu"}>
            <div className={"menu-article-list-wrapper"}>
                <span className={"article-list-header"}>Articles</span>
                <ArticleList />
            </div>
            <div />
        </div>
    );
}
