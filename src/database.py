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
from src.model.task import Task
from src.model.tenant import Tenant
from src.model.user import UserAccount

DATA_COUNT = 25

tenant_list: List[Tenant] = []
user_list: List[UserAccount] = []
person_list: List[Person] = []
task_list: List[Task] = []
calendar_list: List[Calendar] = []

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

# Generate Tenants from the predefined list
for tenant_data in predefined_tenants:
    tenant_list.append(Tenant(id=str(uuid.uuid4()), **tenant_data))

# Generate Users
for i in range(len(user_list), DATA_COUNT):
    t_count = random.randint(0, len(tenant_list) - 1)
    dummy_tenants = []
    for _ in range(t_count):
        current_tenant = tenant_list[random.randint(0, len(tenant_list) - 1)]
        if current_tenant not in dummy_tenants:
            dummy_tenants.append(current_tenant)

    user_list.append(UserAccount(
        id=str(uuid.uuid4()),
        name=f"{random.choice(predefined_first_names)} {random.choice(predefined_last_names)}",
        status=random.randint(0, len(EStatus) - 1),
        tenant=dummy_tenants
    ))

# Generate Persons
for _ in range(DATA_COUNT * 3):
    person_args = {
        "id": str(uuid.uuid4()),
        "first_name": random.choice(predefined_first_names),
        "last_name": random.choice(predefined_last_names),
        "gender": random.choice(list(EGender))
    }

    # 30% chance to associate with a user account
    if random.random() < 0.3 and user_list:
        user = random.choice(user_list)
        person_args["user"] = user
        # Inherit tenant from user if available
        if user.tenant:
            person_args["tenant"] = random.choice(user.tenant)
        else:
            person_args["tenant"] = random.choice(tenant_list)
    else:
        # Assign a random tenant if no user is associated
        person_args["tenant"] = random.choice(tenant_list)

    person_list.append(Person(**person_args))
