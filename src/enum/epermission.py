"""
Defines the EPermission enum for representing granular permissions within tenants.
"""
from enum import Enum


class EPermission(Enum):
    """Represents specific permissions a user can have within a tenant."""
    
    # Person management permissions
    VIEW_PERSONS = "view_persons"
    CREATE_PERSONS = "create_persons"
    EDIT_PERSONS = "edit_persons"
    DELETE_PERSONS = "delete_persons"
    
    # Task management permissions
    VIEW_TASKS = "view_tasks"
    CREATE_TASKS = "create_tasks"
    EDIT_TASKS = "edit_tasks"
    DELETE_TASKS = "delete_tasks"
    
    # Record management permissions
    VIEW_RECORDS = "view_records"
    CREATE_RECORDS = "create_records"
    EDIT_RECORDS = "edit_records"
    DELETE_RECORDS = "delete_records"
    
    # Tag management permissions
    VIEW_TAGS = "view_tags"
    CREATE_TAGS = "create_tags"
    EDIT_TAGS = "edit_tags"
    DELETE_TAGS = "delete_tags"
    
    # Calendar management permissions
    VIEW_CALENDAR = "view_calendar"
    CREATE_CALENDAR = "create_calendar"
    EDIT_CALENDAR = "edit_calendar"
    DELETE_CALENDAR = "delete_calendar"
    
    # User management permissions (admin/owner only)
    VIEW_USERS = "view_users"
    MANAGE_USERS = "manage_users"
    ASSIGN_ROLES = "assign_roles"
    MANAGE_PERMISSIONS = "manage_permissions"
    
    # Tenant management permissions (owner only)
    MANAGE_TENANT = "manage_tenant"
    DELETE_TENANT = "delete_tenant"
    
    # Analytics and reporting
    VIEW_ANALYTICS = "view_analytics"
