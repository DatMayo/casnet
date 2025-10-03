# API: Tenants

This page details the CRUD operations for tenant management.

**Authentication**: All endpoints require a valid JWT bearer token.

---

## Create Tenant

- **Endpoint**: `POST /tenant`
- **Description**: Creates a new tenant.
- **Permissions**: Any authenticated user.

### Request Body

```json
{
  "name": "New Department",
  "description": "A department for special projects."
}
```

### Example Response (Success)

```json
{
  "id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "name": "New Department",
  "description": "A department for special projects."
}
```

---

## List Tenants

- **Endpoint**: `GET /tenant`
- **Description**: Retrieves a paginated list of tenants the current user is a member of.
- **Permissions**: Any authenticated user.

### Query Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `page` | `integer` | `1` | The page number to retrieve. |
| `page_size` | `integer` | `20` | The number of items per page. |

### Example Response

```json
{
  "data": [
    {
      "id": "...",
      "name": "Default Tenant",
      "description": "The default tenant for new users."
    }
  ],
  "meta": {
    "total_items": 1,
    "total_pages": 1,
    "current_page": 1,
    "page_size": 20
  }
}
```

---

## Get Tenant by ID

- **Endpoint**: `GET /tenant/{tenant_id}`
- **Description**: Retrieves the details of a specific tenant.
- **Permissions**: User must be a member of the tenant.

### Path Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `tenant_id` | `string` | **Required**. The ID of the tenant to retrieve. |

### Example Response

(Same as "Create Tenant" response)

---

## Update Tenant

- **Endpoint**: `PUT /tenant/{tenant_id}`
- **Description**: Updates a tenant's details.
- **Permissions**: User must be a member of the tenant.

### Request Body

All fields are optional.

```json
{
  "name": "Updated Department Name",
  "description": "An updated description."
}
```

### Example Response

(Same as "Create Tenant" response)

---

## Delete Tenant

- **Endpoint**: `DELETE /tenant/{tenant_id}`
- **Description**: Deletes a tenant and all associated data (persons, records, etc.).
- **Permissions**: Superuser (or tenant owner - to be implemented).

### Example Response (Success)

```json
{
  "message": "Tenant deleted successfully"
}
```

---

## Manage Tenant Users

### Add User to Tenant

- **Endpoint**: `POST /tenant/{tenant_id}/user/{user_id}`
- **Description**: Adds a user to a tenant.
- **Permissions**: Superuser (or tenant admin).

### Remove User from Tenant

- **Endpoint**: `DELETE /tenant/{tenant_id}/user/{user_id}`
- **Description**: Removes a user from a tenant.
- **Permissions**: Superuser (or tenant admin).
