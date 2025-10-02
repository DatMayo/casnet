from typing import List

from src.model.entity import Entity
from src.model.person import Person
from src.model.tag import Tag
from src.model.tenant import Tenant


class Record(Entity):
    title: str
    description: str
    created_by: Person
    processed_by: Person
    tags: List[Tag]
    additional_processors: List[Person]
    tenant: Tenant = None
