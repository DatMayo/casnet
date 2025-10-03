# API: Records & Tags

This page details the CRUD operations for records (case files) and tags within a specific tenant.

**Authentication**: All endpoints require a valid JWT bearer token.
**Tenant Access**: The authenticated user must be a member of the `{tenant_id}` specified in the URL.

---

## Record Endpoints

### Create Record

- **Endpoint**: `POST /record/{tenant_id}`
- **Description**: Creates a new record.

### List Records

- **Endpoint**: `GET /record/{tenant_id}`
- **Description**: Retrieves a paginated list of records.

### Get, Update, & Delete Record

- **Endpoints**:
  - `GET /record/{tenant_id}/{record_id}`
  - `PUT /record/{tenant_id}/{record_id}`
  - `DELETE /record/{tenant_id}/{record_id}`
- **Description**: Standard GET, PUT, and DELETE operations for a single record.

### Request/Response Structure

The request and response bodies for records follow a structure similar to the [Person](https://github.com/DatMayo/casnet-backend/wiki/API-Persons) model, typically including `title`, `content`, and timestamps.

---

## Tag Endpoints

### Create Tag

- **Endpoint**: `POST /tag/{tenant_id}`
- **Description**: Creates a new tag.

### List Tags

- **Endpoint**: `GET /tag/{tenant_id}`
- **Description**: Retrieves a paginated list of tags.

### Get, Update, & Delete Tag

- **Endpoints**:
  - `GET /tag/{tenant_id}/{tag_id}`
  - `PUT /tag/{tenant_id}/{tag_id}`
  - `DELETE /tag/{tenant_id}/{tag_id}`
- **Description**: Standard GET, PUT, and DELETE operations for a single tag.

---

## Associating Tags with Records

To link a tag to a record, you can include a list of `tag_ids` when creating or updating a record.

### Example: Create Record with Tags

```json
{
  "title": "Case File #123",
  "content": "Details about the case...",
  "tag_ids": [
    "tag_id_1",
    "tag_id_2"
  ]
}
```
