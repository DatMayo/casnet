# API: Tasks & Calendar

This page details the CRUD operations for tasks and calendar events within a specific tenant.

**Authentication**: All endpoints require a valid JWT bearer token.
**Tenant Access**: The authenticated user must be a member of the `{tenant_id}` specified in the URL.

---

## Task Endpoints

Tasks are managed on a per-tenant basis.

### Create Task

- **Endpoint**: `POST /task/{tenant_id}`
- **Description**: Creates a new task.

### List Tasks

- **Endpoint**: `GET /task/{tenant_id}`
- **Description**: Retrieves a paginated list of tasks.

### Get, Update, & Delete Task

- **Endpoints**:
  - `GET /task/{tenant_id}/{task_id}`
  - `PUT /task/{tenant_id}/{task_id}`
  - `DELETE /task/{tenant_id}/{task_id}`
- **Description**: Standard GET, PUT, and DELETE operations for a single task.

### Request/Response Structure

The request and response bodies for tasks typically include fields like `title`, `description`, `due_date`, `status`, and `assignee_id`.

---

## Calendar Event Endpoints

Calendar events are also managed on a per-tenant basis.

### Create Calendar Event

- **Endpoint**: `POST /calendar/{tenant_id}`
- **Description**: Creates a new calendar event.

### List Calendar Events

- **Endpoint**: `GET /calendar/{tenant_id}`
- **Description**: Retrieves a paginated list of calendar events.

### Get, Update, & Delete Calendar Event

- **Endpoints**:
  - `GET /calendar/{tenant_id}/{event_id}`
  - `PUT /calendar/{tenant_id}/{event_id}`
  - `DELETE /calendar/{tenant_id}/{event_id}`
- **Description**: Standard GET, PUT, and DELETE operations for a single calendar event.

### Request/Response Structure

The request and response bodies for calendar events typically include fields like `title`, `description`, `start_time`, `end_time`, and `location`.
