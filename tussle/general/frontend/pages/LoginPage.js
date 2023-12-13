import {PageWrapper} from "../app/PageWrapper";
import React from "react";
import "./LoginPage.scss";
import Button from "@mui/material/Button";
import {useAuth0} from "@auth0/auth0-react";


export function LoginPage() {
    const { loginWithPopup, isAuthenticated } = useAuth0();

    if (isAuthenticated) {

    }

    return <PageWrapper>
        <div className={"login-page"}>
            <Button className={"login-button"} onClick={loginWithPopup} variant={"outlined"}>Login</Button>
        </div>
    </PageWrapper>
}

