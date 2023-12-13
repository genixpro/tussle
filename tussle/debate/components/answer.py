from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass(slots=True, kw_only=True)
class Answer:
    _id: str

    owner: str | None

    topic_id: str | None

    answer: str | None


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
