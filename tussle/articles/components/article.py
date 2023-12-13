from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from .default_prompts import default_paragraph_generating_prompt

@dataclass_json
@dataclass(slots=True, kw_only=True)
class ArticlePrompt:
    id: str

    text: str

    generated: str = ""

    filled_prompt: str = ""

    heading: str = ""

    disable_ai: bool = False


@dataclass_json
@dataclass(slots=True, kw_only=True)
class Article:
    _id: str

    owner: str | None

    # TODO: Rename this to 'sections'
    prompts: list[ArticlePrompt]

    title: str = ""

    slug: str = ""

    question: str = ""

    question_placeholder: str = "Enter your answer here..."

    default_question_answer: str = ""

    date: str = ""

    paragraph_generating_prompt: str = default_paragraph_generating_prompt

    published: bool = False

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
