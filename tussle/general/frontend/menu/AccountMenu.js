import * as React from 'react';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import Logout from '@mui/icons-material/Logout';
import "./AccountMenu.scss";
import { useAuth0 } from "@auth0/auth0-react";
import md5Hex from 'md5-hex';

export default function AccountMenu() {
    const { loginWithPopup, logout, user, isAuthenticated } = useAuth0();

    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleLoginClick = () => {
        loginWithPopup();
    };

    const handleLogoutClick = () => {
        handleClose();
        logout({ logoutParams: { returnTo: window.location.origin } });
    }

    // Generates the gravatar url for the given email address by triming, lowercasing and md5ing it
    let gravatarUrl = null;
    if (user) {
        gravatarUrl = `https://www.gravatar.com/avatar/${md5Hex(user?.email?.trim().toLowerCase())}.jpg?d=mp`;
    }

    let avatarStyle = {
        width: 32,
        height: 32,
    }

    if (user) {
        avatarStyle.bgcolor = "#09a60c";
    }

    return (
        <div className={"account-menu"}>
            <React.Fragment>
                <Box sx={{display: 'flex', alignItems: 'center', textAlign: 'center'}}>
                    <Tooltip title="Account">
                        <IconButton
                            onClick={handleClick}
                            size="small"
                            sx={{ml: 2}}
                            aria-controls={open ? 'account-menu' : undefined}
                            aria-haspopup="true"
                            aria-expanded={open ? 'true' : undefined}
                        >
                            <Avatar sx={avatarStyle} src={gravatarUrl}>
                                {
                                    user ? <span className={"avatar-text"}>{user?.given_name?.substring(0, 1)}{user?.family_name?.substring(0, 1)}</span> : null
                                }
                            </Avatar>
                        </IconButton>
                    </Tooltip>
                </Box>
                <Menu
                    anchorEl={anchorEl}
                    id="account-menu"
                    open={open}
                    onClose={handleClose}
                    onClick={handleClose}
                    PaperProps={{
                        elevation: 0,
                        sx: {
                            overflow: 'visible',
                            filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                            mt: 1.5,
                            '& .MuiAvatar-root': {
                                width: 32,
                                height: 32,
                                ml: -0.5,
                                mr: 1,
                            },
                            '&:before': {
                                content: '""',
                                display: 'block',
                                position: 'absolute',
                                top: 0,
                                right: 14,
                                width: 10,
                                height: 10,
                                bgcolor: 'background.paper',
                                transform: 'translateY(-50%) rotate(45deg)',
                                zIndex: 0,
                            },
                        },
                    }}
                    transformOrigin={{horizontal: 'right', vertical: 'top'}}
                    anchorOrigin={{horizontal: 'right', vertical: 'bottom'}}
                >
                    {
                        !isAuthenticated ?
                            <MenuItem onClick={handleLoginClick}>
                                <Avatar/> Login
                            </MenuItem>
                            : null
                    }
                    {
                        isAuthenticated ?
                            <MenuItem>
                                {user?.name}
                            </MenuItem>
                            : null
                    }
                    {
                        isAuthenticated ?
                            <MenuItem>
                                {user?.email}
                            </MenuItem>
                            : null
                    }
                    {
                        isAuthenticated ?
                            <MenuItem onClick={handleLogoutClick}>
                                <ListItemIcon>
                                    <Logout fontSize="small"/>
                                </ListItemIcon>
                                Logout
                            </MenuItem> : null
                    }
                </Menu>
            </React.Fragment>
        </div>
    );
}