import React from "react";
import "./Footer.scss";
import Typography from "@mui/material/Typography";
import Popover from "@mui/material/Popover";


export function Footer() {
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const open = Boolean(anchorEl);
    const id = open ? 'simple-popover' : undefined;

    return <div className={"footer"}>
        <span onClick={handleClick}>Get Tussle for your business</span>
        <a href={"https://www.bradleyarsenault.me/"} target="_blank" rel="noreferrer">Learn more about Brad</a>
        <Popover
            id={id}
            open={open}
            anchorEl={anchorEl}
            onClose={handleClose}
            anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
            }}
        >
            <Typography sx={{p: 2}}>
                Tussle is a custom tool originally built by Bradley Arsenault for his own blog.<br/>
                To get Tussle at your business, please contact Bradley Arsenault to setup an<br/>
                installation on your own domain name and to customize the look and feel to your<br/>
                needs.<br/>
                <a href={"https://www.bradleyarsenault.me/contact-me"} target="_blank" rel="noreferrer">Contact Brad</a>
            </Typography>
        </Popover>
    </div>
}
