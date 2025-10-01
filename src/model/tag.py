from src.model.entity import Entity
from src.model.person import Person


class Tag(Entity):
    name: str
    color: str
    created_by: Person
