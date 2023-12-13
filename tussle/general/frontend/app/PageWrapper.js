import {TopBar} from "../menu/TopBar";
import LeftSideMenu from "../menu/LeftSideMenu";
import React from "react";
import {Footer} from "./Footer";

export const PageWrapper = ({children}) => {
    return <div className="App">
        <TopBar/>
        <div className={"below-top-bar"}>

            <LeftSideMenu/>

            <div className={"main-content-area"}>
                <div className={"main-content-area-inner"}>
                    {children}
                </div>

                <Footer />
            </div>
        </div>
    </div>
};