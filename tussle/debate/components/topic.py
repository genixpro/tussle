from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass(slots=True, kw_only=True)
class Topic:
    _id: str

    owner: str | None

    description: str | None


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
