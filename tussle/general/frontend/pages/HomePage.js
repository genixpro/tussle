import {PageWrapper} from "../app/PageWrapper";
import {useEffect} from "react";
import {useNavigate} from "react-router-dom";
import "./HomePage.scss";


export function HomePage() {
    const navigate = useNavigate();

    useEffect(() => {
        navigate("/article/what-is-the-dataset-hustle");
    }, [navigate]);


    // Don't do anything on the home except redirect to a valid article slug.
    return <PageWrapper>

    </PageWrapper>
}

