"""
In-memory database for the application.

This module initializes and populates in-memory lists of data models with dummy
data for demonstration purposes. In a production environment, this would be replaced
with a proper database connection.
"""
import random
import uuid
from typing import List

from src.enum.egender import EGender
from src.enum.estatus import EStatus
from src.model.calendar import Calendar
from src.model.person import Person
from src.model.record import Record
from src.model.tag import Tag
from src.model.task import Task
from src.model.tenant import Tenant
from src.model.user import UserAccount
from src.security import get_password_hash


tenant_list: List[Tenant] = []
user_list: List[UserAccount] = []
person_list: List[Person] = []
task_list: List[Task] = []
calendar_list: List[Calendar] = []
record_list: List[Record] = []
tag_list: List[Tag] = []

DATA_COUNT = 25

predefined_tenants = [
    {"name": "LSPD", "description": "Los Santos Police Department"},
    {"name": "SAFMS", "description": "San Andreas Medical Service"},
    {"name": "BCSO", "description": "Blaine County Sheriff's Office"},
    {"name": "SASP", "description": "San Andreas State Police"},
    {"name": "DOJ", "description": "Department of Justice"},
    {"name": "FIB", "description": "Federal Investigation Bureau"},
    {"name": "IAA", "description": "Internal Affairs Agency"},
    {"name": "LSC", "description": "Los Santos Customs"},
    {"name": "LSFD", "description": "Los Santos Fire Department"},
    {"name": "LST", "description": "Los Santos Transit"},
    {"name": "PDM", "description": "Premium Deluxe Motorsport"},
    {"name": "LSCG", "description": "Los Santos Coast Guard"},
    {"name": "SAHP", "description": "San Andreas Highway Patrol"},
    {"name": "SADCR", "description": "San Andreas Dept. of Corrections and Rehabilitation"},
    {"name": "SANG", "description": "San Andreas National Guard"},
    {"name": "LSPA", "description": "Los Santos Port Authority"},
    {"name": "LSIA", "description": "Los Santos International Airport"},
    {"name": "ULS", "description": "University of Los Santos"},
    {"name": "GOH", "description": "Galileo Observatory House"},
    {"name": "VGH", "description": "Vespucci General Hospital"},
    {"name": "PSH", "description": "Pillbox Hill Medical Center"},
    {"name": "DWP", "description": "Department of Water and Power"},
    {"name": "DPR", "description": "Department of Parks and Recreation"},
    {"name": "DOT", "description": "Department of Transportation"},
    {"name": "DCH", "description": "Davis County Hospital"}
]

predefined_first_names = [
    "Alex", "Jamie", "Chris", "Pat", "Taylor", "Jordan", "Casey", "Morgan", "Riley", "Skyler",
    "Michael", "Jessica", "Matthew", "Ashley", "Christopher", "Emily", "Joshua", "Samantha",
    "David", "Amanda", "Daniel", "Brittany", "Robert", "Megan", "Joseph", "Jennifer", "Andrew",
    "Nicole", "Ryan", "Stephanie"
]

predefined_last_names = [
    "Jones", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas",
    "Smith", "Johnson", "Garcia", "Martinez", "Rodriguez", "Hernandez", "Lopez", "Gonzalez", "Perez",
    "Sanchez", "Ramirez", "Clark", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "King", "Wright"
]

predefined_calendar_titles = [
    "Project Alpha Kick-off", "Quarterly Review", "Team Sync", "Client Demo", "Marketing Brainstorm",
    "Security Audit", "Performance Review", "API Design Session", "Database Migration Plan"
]

predefined_task_titles = [
    "Deploy to Staging", "Fix Login Bug", "Update Documentation", "Refactor API Endpoint",
    "Write Unit Tests for User Service", "Design New Dashboard UI", "Investigate Memory Leak"
]

predefined_record_titles = [
    "Incident Report #102", "Case File #482", "Evidence Log #991", "Traffic Stop Recording #A45",
    "Internal Affairs Complaint #C78", "Field Interview #F32"
]

predefined_tag_data = [
    {"name": "Urgent", "color": "#FF0000"},
    {"name": "Low Priority", "color": "#00FF00"},
    {"name": "Bug", "color": "#FFA500"},
    {"name": "Feature Request", "color": "#0000FF"},
    {"name": "Investigation", "color": "#800080"},
    {"name": "Civilian Report", "color": "#FFFF00"}
]

# Generate Tenants from the predefined list
for tenant_data in predefined_tenants:
    tenant_list.append(Tenant(id=str(uuid.uuid4()), **tenant_data))

# Generate Users, Persons, and other data
for i in range(DATA_COUNT * 3):
    # Assign a tenant
    tenant = random.choice(tenant_list)

    # Create a user with a chance of having multiple tenants
    t_count = random.randint(1, 3)
    dummy_tenants = random.sample(tenant_list, t_count)
    user = UserAccount(
        id=str(uuid.uuid4()),
        name=f"{random.choice(predefined_first_names)} {random.choice(predefined_last_names)}",
        hashed_password=get_password_hash("password"),
        status=random.randint(0, len(EStatus) - 1),
        tenant=dummy_tenants
    )
    user_list.append(user)

    # Create a person associated with the user and a primary tenant
    person = Person(
        id=str(uuid.uuid4()),
        first_name=random.choice(predefined_first_names),
        last_name=random.choice(predefined_last_names),
        gender=random.choice(list(EGender)),
        user=user,
        tenant=tenant
    )
    person_list.append(person)

    # Create other data associated with the person and tenant
    calendar_list.append(Calendar(
        id=str(uuid.uuid4()),
        title=random.choice(predefined_calendar_titles),
        description=f"Discussion about {random.choice(predefined_task_titles)}",
        created_from=person,
        date_start=random.randint(1672531200, 1675209600),
        date_end=random.randint(1675209600, 1677888000),
        tenant=tenant
    ))

    task_list.append(Task(
        id=str(uuid.uuid4()),
        title=random.choice(predefined_task_titles),
        created_from=person,
        created_for=random.choice(person_list) if person_list else person,
        tenant=tenant
    ))

    tag_data = random.choice(predefined_tag_data)
    tag = Tag(
        id=str(uuid.uuid4()),
        name=tag_data["name"],
        color=tag_data["color"],
        created_by=person,
        tenant=tenant
    )
    tag_list.append(tag)

    record_list.append(Record(
        id=str(uuid.uuid4()),
        title=random.choice(predefined_record_titles),
        description=f"Details regarding {random.choice(predefined_record_titles)}",
        created_by=person,
        processed_by=random.choice(person_list) if person_list else person,
        tags=[tag],
        additional_processors=[random.choice(person_list) for _ in range(random.randint(0, 2)) if person_list],
        tenant=tenant
    ))
