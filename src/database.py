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
from src.models import Base, User, Tenant
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
    Create the default admin account if it doesn't exist.
    
    Args:
        db: Database session
        
    Returns:
        User: The admin user account
    """
    # Check if admin account already exists
    admin = db.query(User).filter(User.name == "admin").first()
    if admin:
        logger.info("👤 Admin account already exists")
        return admin
    
    # Create default admin account
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


def create_default_tenant_and_assignment(db: Session) -> Tenant:
    """
    Create a default tenant and assign the admin user to it.
    
    Args:
        db: Database session
        
    Returns:
        Tenant: The default tenant
    """
    # Check if default tenant already exists
    default_tenant = db.query(Tenant).filter(Tenant.name == "Default Organization").first()
    if default_tenant:
        logger.info("🏢 Default tenant already exists")
        return default_tenant
    
    # Create default tenant
    default_tenant = Tenant(
        name="Default Organization",
        description="Default tenant for initial system setup and administration",
        status=1  # Active
    )
    db.add(default_tenant)
    db.commit()
    db.refresh(default_tenant)
    
    # Assign admin user to default tenant
    admin_user = db.query(User).filter(User.name == "admin").first()
    if admin_user and admin_user not in default_tenant.users:
        default_tenant.users.append(admin_user)
        db.commit()
        logger.info("👤 Admin user assigned to default tenant")
    
    logger.info("🏢 Default tenant created and admin assigned")
    return default_tenant


def initialize_database():
    """
    Initialize the database by creating tables, default admin account, and default tenant.
    This function is called on application startup.
    """
    # Create tables
    create_tables()
    
    # Create default admin account and tenant
    with SessionLocal() as db:
        create_default_admin_account(db)
        create_default_tenant_and_assignment(db)
    
    # Log completion
    total_time = time.time() - start_time
    logger.info(f"✅ Database initialization complete! Total time: {total_time:.2f}s")


# Initialize database on module import
initialize_database()
