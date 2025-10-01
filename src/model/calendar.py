from src.model.entity import Entity
from src.model.person import Person


class Calendar(Entity):
    title: str
    description: str = None
    created_from: Person
    date_start: int
    date_end: int = 0
