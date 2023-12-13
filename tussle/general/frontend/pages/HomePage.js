import {PageWrapper} from "../app/PageWrapper";
import {useEffect} from "react";
import {useNavigate} from "react-router-dom";
import "./HomePage.scss";
import {DebatePage} from "../../../debate/frontend/DebatePage";


export function HomePage() {
    const navigate = useNavigate();

    // Load up the debate page
    return <PageWrapper>
        <DebatePage />
    </PageWrapper>
}

