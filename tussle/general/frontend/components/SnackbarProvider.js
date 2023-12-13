import React, {useContext} from "react";
import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";


const SnackbarContext = React.createContext(null);
export const SnackbarProvider = ({children}) => {
    const [open, setOpen] = React.useState(false);
    const [message, setMessage] = React.useState("");
    const [severity, setSeverity] = React.useState("success");
    const [autoHideMs, setAutoHideMs] = React.useState(5000);

    const snackbarInterface = {
        toast: ({message, severity, autoHideMs}) => {
            setOpen(true);
            setMessage(message);
            setSeverity(severity);
            setAutoHideMs(autoHideMs);
        }
    }

    const handleClose = (event) => {
        setOpen(false);
    };

    return <SnackbarContext.Provider value={snackbarInterface}>
        {children}

        <Snackbar
            open={open}
            autoHideDuration={autoHideMs}
            onClose={handleClose}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        >
            <Alert onClose={handleClose} severity={severity} sx={{ width: '100%' }}>
                {message}
            </Alert>
        </Snackbar>
    </SnackbarContext.Provider>
};

export const useSnackbar = useContext.bind(null, SnackbarContext);

