"""
API endpoints for authentication and token management.

This module contains authentication endpoints:
- POST /auth/login - Authenticate user and get JWT access token
- POST /auth/logout - Logout current user (client-side token removal)
- POST /auth/refresh - Refresh current user's access token
- GET /auth/me - Get current authenticated user information with tenants
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User
from src.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_password, get_current_user
from src.dependencies import get_permission_service_dep
from src.permissions import PermissionService
from src.schemas.user import UserResponse, UserDetailedResponse
from src.schemas.permission import UserEffectivePermissions

router = APIRouter()


def get_user(username: str, db: Session) -> User:
    """Retrieve a user from the database by their username."""
    return db.query(User).filter(User.name == username).first()


@router.post("/login", tags=["authentication"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate a user and return a JWT access token.
    
    **Endpoint**: `POST /auth/login`
    
    **Request Body** (form data):
    - username: User's login name
    - password: User's password
    
    **Response**:
    - access_token: JWT token for API authentication
    - token_type: Always "bearer"
    - expires_in: Token expiration time in seconds
    
    **Usage**: Include the token in subsequent requests:
    `Authorization: Bearer {access_token}`
    """
    from src.exceptions import InvalidCredentialsError
    
    user = get_user(form_data.username, db)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise InvalidCredentialsError()
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
    }


@router.get("/me", response_model=UserDetailedResponse, tags=["authentication"])
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service_dep)
):
    """
    Get information about the currently authenticated user with roles and permissions.
    
    **Endpoint**: `GET /auth/me`
    
    **Authentication**: Required (Bearer token)
    
    **Response**: Complete user profile including:
    - User ID and username
    - Account timestamps (created_at, updated_at)
    - Detailed tenant access with roles and effective permissions for each tenant
    
    **Frontend Usage Examples**:
    - Display current user name in UI header
    - Populate tenant dropdown/selector with role information
    - Implement role-based access control and UI permissions
    - Show/hide features based on user permissions
    - Role badges and permission indicators
    
    **RBAC Information Returned**:
    - User's role in each tenant (OWNER/ADMIN/USER)
    - Complete list of effective permissions per tenant
    - Combines role-based + directly assigned permissions
    
    **Security**: Only returns data for the authenticated user.
    """
    from src.schemas.user import UserTenantInfo
    from src.schemas.tenant import TenantResponse
    
    # Build detailed tenant access information
    tenant_access = []
    for tenant_role in current_user.tenant_roles:
        tenant = tenant_role.tenant
        effective_permissions = list(permission_service.get_user_effective_permissions(
            current_user.id, tenant.id
        ))
        
        tenant_info = UserTenantInfo(
            tenant=TenantResponse(
                id=tenant.id,
                name=tenant.name,
                description=tenant.description,
                status=tenant.status,
                created_at=tenant.created_at,
                updated_at=tenant.updated_at
            ),
            role=tenant_role.role,
            effective_permissions=effective_permissions
        )
        tenant_access.append(tenant_info)
    
    return UserDetailedResponse(
        id=current_user.id,
        name=current_user.name,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        tenant_access=tenant_access
    )


@router.get("/me/permissions/{tenant_id}", response_model=UserEffectivePermissions, tags=["authentication"])
async def get_user_permissions_for_tenant(
    tenant_id: str,
    current_user: User = Depends(get_current_user),
    permission_service: PermissionService = Depends(get_permission_service_dep)
):
    """
    Get current user's effective permissions for a specific tenant.
    
    **Endpoint**: `GET /auth/me/permissions/{tenant_id}`
    
    **Authentication**: Required (Bearer token)
    
    **Response**: Complete permission breakdown for the specified tenant:
    - User's role in the tenant
    - Permissions from role (inherited)
    - Direct permissions (specifically assigned)
    - Effective permissions (combined total)
    
    **Frontend Usage**:
    - Check if user can perform specific actions
    - Show/hide UI elements based on permissions
    - Implement fine-grained access control
    
    **Example Frontend Logic**:
    ```javascript
    const permissions = await getUserPermissions(tenantId);
    if (permissions.effective_permissions.includes('CREATE_PERSONS')) {
        showCreatePersonButton();
    }
    ```
    """
    # Check if user has access to this tenant
    if not permission_service.user_can_access_tenant(current_user.id, tenant_id):
        raise HTTPException(
            status_code=403,
            detail=f"Access denied: You don't have access to tenant {tenant_id}"
        )
    
    user_role = permission_service.get_user_role_in_tenant(current_user.id, tenant_id)
    role_permissions = list(permission_service.get_role_permissions(user_role)) if user_role else []
    direct_permissions = list(permission_service.get_user_direct_permissions(current_user.id, tenant_id))
    effective_permissions = list(permission_service.get_user_effective_permissions(current_user.id, tenant_id))
    
    return UserEffectivePermissions(
        user_id=current_user.id,
        tenant_id=tenant_id,
        role=user_role,
        role_permissions=role_permissions,
        direct_permissions=direct_permissions,
        effective_permissions=effective_permissions
    )


@router.post("/logout", tags=["authentication"])
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout the current user.
    
    **Endpoint**: `POST /auth/logout`
    
    **Authentication**: Required (Bearer token)
    
    **Note**: With JWT tokens, logout is typically handled client-side by:
    1. Removing the token from client storage (localStorage, cookies, etc.)
    2. Optionally calling this endpoint for server-side logging/analytics
    
    **Response**: Success confirmation message
    """
    return {"message": "Successfully logged out", "user": current_user.name}


@router.post("/refresh", tags=["authentication"])
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """
    Refresh the current user's access token.
    
    **Endpoint**: `POST /auth/refresh`
    
    **Authentication**: Required (Bearer token)
    
    **Response**: New access token with updated expiration
    - access_token: New JWT token for API authentication
    - token_type: Always "bearer"
    - expires_in: Token expiration time in seconds
    
    **Usage**: Replace the old token with the new one in client storage
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.name}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer", 
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
    }
