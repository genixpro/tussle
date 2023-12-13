import './App.scss';
import {HTML5Backend} from 'react-dnd-html5-backend'
import {DndProvider} from 'react-dnd'
import ErrorBoundary from "../components/ErrorBoundary";
import React, {useEffect} from 'react';
import {useAuth0} from '@auth0/auth0-react';
import axios from "axios";
import {createBrowserRouter, RouterProvider,} from "react-router-dom";
import {apiAccessTokenContext} from "../components/api";
import {HomePage} from "../pages/HomePage";
import {SnackbarProvider} from "../components/SnackbarProvider";
import {LoginPage} from "../pages/LoginPage";

const router = createBrowserRouter([
    {
        path: "/",
        element: <HomePage />,
    },
    {
        path: "/login",
        element: <LoginPage />,
    },
]);

function App() {
    const {user, isAuthenticated, getAccessTokenSilently} = useAuth0();
    const [apiAccessToken, setApiAccessToken] = React.useState(null);

    // TODO: This login flow is buggy and not working very well. It requires random popup windows that
    // appear and disappear. It's not very user friendly. I need to find a better way to do this.
    useEffect(() => {
        const getUserMetadata = async () => {
            try {
                const accessToken = await getAccessTokenSilently({
                    audience: process.env.REACT_APP_AUTH0_AUDIENCE,
                });
                setApiAccessToken(accessToken);
                axios.defaults.headers.common['WWW-Authenticate'] = accessToken;

            } catch (e) {
                console.log(e.message);
            }
        };

        if (isAuthenticated) {
            getUserMetadata();
        }
    }, [isAuthenticated, getAccessTokenSilently, user?.sub]);

    if(isAuthenticated && !apiAccessToken) {
        return null;
    }

    return (
        <ErrorBoundary>
            <DndProvider backend={HTML5Backend}>
                <SnackbarProvider>
                    <apiAccessTokenContext.Provider value={apiAccessToken}>
                        <RouterProvider router={router}/>
                    </apiAccessTokenContext.Provider>
                </SnackbarProvider>
            </DndProvider>
        </ErrorBoundary>
    );
}

export default App;
