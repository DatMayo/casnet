# API: Authentication

This page details the process for authenticating with the Casnet Backend API to obtain a JSON Web Token (JWT).

## Get Access Token

- **Endpoint**: `POST /token`
- **Description**: Authenticates a user with their username and password and returns a JWT.
- **Permissions**: Public

### Request Body

The request must be sent with a `Content-Type` of `application/x-www-form-urlencoded`.

| Parameter | Type | Description |
| --- | --- | --- |
| `username` | `string` | **Required**. The user's username. |
| `password` | `string` | **Required**. The user's password. |

### Example Request (cURL)

```bash
curl -X POST "http://127.0.0.1:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=changeme"
```

### Example Response (Success)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Example Response (Error)

```json
{
  "detail": "Incorrect username or password"
}
```

## Using the Access Token

Once you have the `access_token`, you must include it in the `Authorization` header of all subsequent requests to protected endpoints.

- **Header**: `Authorization: Bearer <your_token>`

### Example (cURL)

```bash
curl -X GET "http://127.0.0.1:8000/user/me" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```
