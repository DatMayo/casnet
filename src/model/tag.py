from src.model.entity import Entity
from src.model.person import Person
from src.model.tenant import Tenant


class Tag(Entity):
    name: str
    color: str
    created_by: Person
    tenant: Tenant = None
