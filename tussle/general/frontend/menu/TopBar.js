import "./TopBar.scss";
import AccountMenu from "./AccountMenu";
import {useAuth0} from "@auth0/auth0-react";

export function TopBar() {
    const {isAuthenticated} = useAuth0();

    return <div className={"top-bar"}>

        <div className={"logo-area"}>
            <div className={"logo-image"}>
                <img src={"/logo.png"} alt={"logo"} className={"logo-image"}/>
            </div>

            <span className={"logo-text"}>Articulon</span>
        </div>


        {
            isAuthenticated ?
                <AccountMenu/>
                : null
        }
    </div>
}
