import {NavLink} from "react-router-dom";
import * as React from "react";
import ListItem from "@mui/material/ListItem";
import DescriptionIcon from "@mui/icons-material/Description";
import {useAuth0} from "@auth0/auth0-react";


export function ArticleListItem({article}) {
    const { isAuthenticated } = useAuth0();

    let navLinkClasses = "article-list-item";
    if (!article.title) {
        navLinkClasses += " unnamed";
    }

    return <ListItem key={article._id} disablePadding onClick={(evt) => {
        evt.stopPropagation()
    }}>
        <NavLink
            to={isAuthenticated ? `/article/${article._id}` : `/article/${article.slug}`}
            className={({isActive, isPending}) => {
                const stateClass = isActive ? "active" : isPending ? "pending" : "";
                return navLinkClasses + " " + stateClass;
            }}
        >
            <div className={"title-icon-group"}>
                <DescriptionIcon sx={{fontSize: 25}}/>

                {
                    article.title && <span className={"article-title"}>{article.title}</span>
                }
                {
                    !article.title && <span className={"article-title"}>Unnamed...</span>
                }
            </div>
        </NavLink>
    </ListItem>
}