"""
SQLAlchemy database configuration and initialization.

This module handles SQLite database connection, session management, 
and creates the default admin account on first startup.
"""
import logging
import time
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config import settings
from src.models import Base, User, Tenant, RolePermission, UserTenantRole
from src.enum.erole import ERole
from src.enum.epermission import EPermission
from src.hashing import get_password_hash

# Configure logging for database initialization
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("🚀 Starting database initialization...")
start_time = time.time()

# Create database directory if it doesn't exist
database_path = Path(settings.database_url.replace("sqlite:///", ""))
database_path.parent.mkdir(parents=True, exist_ok=True)

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
    logger.info("📊 Database tables created successfully")


def create_default_admin_account(db: Session) -> User:
    """
    Create the default admin account only if no users exist in the database.
    
    Args:
        db: Database session
        
    Returns:
        User: The admin user account or None if users already exist
    """
    # Check if any users exist in the database
    user_count = db.query(User).count()
    if user_count > 0:
        logger.info("👤 Users already exist in database, skipping default admin creation")
        return db.query(User).first()  # Return first user for consistency
    
    # Create default admin account (only when database is empty)
    hashed_password = get_password_hash("changeme")
    admin = User(
        name="admin",
        hashed_password=hashed_password
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    logger.info("👤 Default admin account created (admin/changeme)")
    return admin


def create_default_role_permissions(db: Session):
    """
    Create default role-permission mappings if they don't exist.
    
    Args:
        db: Database session
    """
    # Check if role permissions already exist
    existing_count = db.query(RolePermission).count()
    if existing_count > 0:
        logger.info("🔐 Role permissions already exist, skipping creation")
        return
    
    # Define default role-permission mappings
    role_permission_mappings = {
        ERole.OWNER: [
            # All permissions for owners
            EPermission.VIEW_PERSONS, EPermission.CREATE_PERSONS, EPermission.EDIT_PERSONS, EPermission.DELETE_PERSONS,
            EPermission.VIEW_TASKS, EPermission.CREATE_TASKS, EPermission.EDIT_TASKS, EPermission.DELETE_TASKS,
            EPermission.VIEW_RECORDS, EPermission.CREATE_RECORDS, EPermission.EDIT_RECORDS, EPermission.DELETE_RECORDS,
            EPermission.VIEW_TAGS, EPermission.CREATE_TAGS, EPermission.EDIT_TAGS, EPermission.DELETE_TAGS,
            EPermission.VIEW_CALENDAR, EPermission.CREATE_CALENDAR, EPermission.EDIT_CALENDAR, EPermission.DELETE_CALENDAR,
            EPermission.VIEW_USERS, EPermission.MANAGE_USERS, EPermission.ASSIGN_ROLES, EPermission.MANAGE_PERMISSIONS,
            EPermission.MANAGE_TENANT, EPermission.DELETE_TENANT, EPermission.VIEW_ANALYTICS
        ],
        ERole.ADMIN: [
            # Most permissions for admins (excluding tenant management)
            EPermission.VIEW_PERSONS, EPermission.CREATE_PERSONS, EPermission.EDIT_PERSONS, EPermission.DELETE_PERSONS,
            EPermission.VIEW_TASKS, EPermission.CREATE_TASKS, EPermission.EDIT_TASKS, EPermission.DELETE_TASKS,
            EPermission.VIEW_RECORDS, EPermission.CREATE_RECORDS, EPermission.EDIT_RECORDS, EPermission.DELETE_RECORDS,
            EPermission.VIEW_TAGS, EPermission.CREATE_TAGS, EPermission.EDIT_TAGS, EPermission.DELETE_TAGS,
            EPermission.VIEW_CALENDAR, EPermission.CREATE_CALENDAR, EPermission.EDIT_CALENDAR, EPermission.DELETE_CALENDAR,
            EPermission.VIEW_USERS, EPermission.MANAGE_USERS, EPermission.ASSIGN_ROLES, EPermission.MANAGE_PERMISSIONS,
            EPermission.VIEW_ANALYTICS
        ],
        ERole.USER: [
            # Basic permissions for regular users
            EPermission.VIEW_PERSONS, EPermission.CREATE_PERSONS, EPermission.EDIT_PERSONS,
            EPermission.VIEW_TASKS, EPermission.CREATE_TASKS, EPermission.EDIT_TASKS,
            EPermission.VIEW_RECORDS, EPermission.CREATE_RECORDS, EPermission.EDIT_RECORDS,
            EPermission.VIEW_TAGS, EPermission.CREATE_TAGS, EPermission.EDIT_TAGS,
            EPermission.VIEW_CALENDAR, EPermission.CREATE_CALENDAR, EPermission.EDIT_CALENDAR
        ]
    }
    
    # Create role-permission mappings
    for role, permissions in role_permission_mappings.items():
        for permission in permissions:
            role_perm = RolePermission(role=role, permission=permission)
            db.add(role_perm)
    
    db.commit()
    total_mappings = sum(len(perms) for perms in role_permission_mappings.values())
    logger.info(f"🔐 Created {total_mappings} role-permission mappings")


def create_default_tenant_and_assignment(db: Session) -> Tenant:
    """
    Create a default tenant only if no tenants exist in the database.
    Assign the first user to the default tenant if created.
    
    Args:
        db: Database session
        
    Returns:
        Tenant: The default tenant or None if tenants already exist
    """
    # Check if any tenants exist in the database
    tenant_count = db.query(Tenant).count()
    if tenant_count > 0:
        logger.info("🏢 Tenants already exist in database, skipping default tenant creation")
        return db.query(Tenant).first()  # Return first tenant for consistency
    
    # Create default tenant (only when database is empty)
    default_tenant = Tenant(
        name="Default Organization",
        description="Default tenant for initial system setup and administration",
        status=1  # Active
    )
    db.add(default_tenant)
    db.commit()
    db.refresh(default_tenant)
    
    # Assign first user as OWNER of the default tenant
    first_user = db.query(User).first()
    if first_user:
        # Check if user already has a role in this tenant
        existing_role = db.query(UserTenantRole).filter(
            UserTenantRole.user_id == first_user.id,
            UserTenantRole.tenant_id == default_tenant.id
        ).first()
        
        if not existing_role:
            user_role = UserTenantRole(
                user_id=first_user.id,
                tenant_id=default_tenant.id,
                role=ERole.OWNER
            )
            db.add(user_role)
            db.commit()
            logger.info("👤 First user assigned as OWNER of default tenant")
    
    logger.info("🏢 Default tenant created and admin user assigned as owner")
    return default_tenant


def initialize_database():
    """
    Initialize the database by creating tables, default admin account, default tenant,
    and role-permission mappings. This function is called on application startup.
    """
    # Create tables
    create_tables()
    
    # Create default data
    with SessionLocal() as db:
        create_default_role_permissions(db)
        create_default_admin_account(db)
        create_default_tenant_and_assignment(db)
    
    # Log completion
    total_time = time.time() - start_time
    logger.info(f"✅ Database initialization complete! Total time: {total_time:.2f}s")


# Initialize database on module import
initialize_database()
