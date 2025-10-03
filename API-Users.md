# API: Users

This page details the CRUD operations for user management.

**Authentication**: All endpoints require a valid JWT bearer token.

---

## Create User

- **Endpoint**: `POST /user`
- **Description**: Creates a new user account.
- **Permissions**: Superuser

### Request Body

```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "full_name": "New User",
  "password": "a_strong_password"
}
```

### Example Response (Success)

```json
{
  "id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "username": "newuser",
  "email": "newuser@example.com",
  "full_name": "New User",
  "is_active": true,
  "is_superuser": false
}
```

---

## Get Current User

- **Endpoint**: `GET /user/me`
- **Description**: Retrieves the details of the currently authenticated user.
- **Permissions**: Any authenticated user.

### Example Response

```json
{
  "id": "...",
  "username": "admin",
  "email": "admin@example.com",
  "full_name": "Admin User",
  "is_active": true,
  "is_superuser": true,
  "tenants": [
    {
      "id": "...",
      "name": "Default Tenant"
    }
  ]
}
```

---

## Get User by ID

- **Endpoint**: `GET /user/{user_id}`
- **Description**: Retrieves the details of a specific user.
- **Permissions**: Superuser

### Path Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `user_id` | `string` | **Required**. The ID of the user to retrieve. |

### Example Response

(Same as "Get Current User")

---

## List Users

- **Endpoint**: `GET /user`
- **Description**: Retrieves a paginated list of all users.
- **Permissions**: Superuser

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
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "Admin User"
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

## Update User

- **Endpoint**: `PUT /user/{user_id}`
- **Description**: Updates a user's details.
- **Permissions**: Superuser, or the user themselves.

### Request Body

All fields are optional.

```json
{
  "email": "new.email@example.com",
  "full_name": "Updated Name"
}
```

### Example Response

(Same as "Get Current User")

---

## Delete User

- **Endpoint**: `DELETE /user/{user_id}`
- **Description**: Deletes a user account.
- **Permissions**: Superuser

### Example Response (Success)

```json
{
  "message": "User deleted successfully"
}
```
