import React, {useState} from 'react';
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import "./ArticleQuestion.scss";

export default function ArticleQuestion({article, onDone}) {
    const [answer, setAnswer] = useState('');

    const handleAnswerChange = (event) => {
        setAnswer(event.target.value);
    };

    const onUseDefaultClicked = () => {
        setAnswer(article.default_question_answer);
    };

    return (
        <>
            <div className={"article-question"}>
                <Card className={"article-card"}>
                    <CardContent>
                        <Typography variant="h6" component="div">
                            {article.question}
                        </Typography>
                        <TextField
                            multiline
                            rows={2}
                            variant="outlined"
                            value={answer}
                            onChange={handleAnswerChange}
                            placeholder={article.question_placeholder}
                        />
                        <Button
                            variant="contained"
                            color="success"
                            onClick={onUseDefaultClicked}
                        >
                            Use Default
                        </Button>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={() => onDone(answer)}
                        >
                            Done
                        </Button>
                    </CardContent>
                </Card>
            </div>
        </>
    );
}