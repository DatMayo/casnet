# API: Persons

This page details the CRUD operations for person profiles within a specific tenant.

**Authentication**: All endpoints require a valid JWT bearer token.
**Tenant Access**: The authenticated user must be a member of the `{tenant_id}` specified in the URL.

---

## Create Person

- **Endpoint**: `POST /person/{tenant_id}`
- **Description**: Creates a new person profile within a tenant.

### Path Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `tenant_id` | `string` | **Required**. The ID of the tenant where the person will be created. |

### Request Body

```json
{
  "name": "John Doe",
  "date_of_birth": "1990-01-01",
  "gender": "MALE",
  "contact_info": {
    "phone": "123-456-7890",
    "address": "123 Main St"
  }
}
```

### Example Response (Success)

```json
{
  "id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
  "tenant_id": "...",
  "name": "John Doe",
  "date_of_birth": "1990-01-01",
  "gender": "MALE",
  "contact_info": {
    "phone": "123-456-7890",
    "address": "123 Main St"
  }
}
```

---

## List Persons

- **Endpoint**: `GET /person/{tenant_id}`
- **Description**: Retrieves a paginated list of all person profiles within a tenant.

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
      "name": "John Doe",
      "date_of_birth": "1990-01-01"
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

## Get Person by ID

- **Endpoint**: `GET /person/{tenant_id}/{person_id}`
- **Description**: Retrieves the details of a specific person profile.

### Path Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `tenant_id` | `string` | **Required**. The ID of the tenant. |
| `person_id` | `string` | **Required**. The ID of the person to retrieve. |

### Example Response

(Same as "Create Person" response)

---

## Update Person

- **Endpoint**: `PUT /person/{tenant_id}/{person_id}`
- **Description**: Updates a person's details.

### Request Body

All fields are optional.

```json
{
  "name": "Johnathan Doe",
  "contact_info": {
    "phone": "987-654-3210"
  }
}
```

### Example Response

(Same as "Create Person" response)

---

## Delete Person

- **Endpoint**: `DELETE /person/{tenant_id}/{person_id}`
- **Description**: Deletes a person profile.

### Example Response (Success)

```json
{
  "message": "Person deleted successfully"
}
```
