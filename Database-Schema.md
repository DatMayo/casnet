# Database Schema

This document provides a detailed overview of the database schema used in the Casnet Backend API. The application uses SQLAlchemy 2.0 to define and interact with the database models.

## Overview

The schema is designed around a multi-tenant architecture. The core models are `User` and `Tenant`. Most other data models, such as `Person`, `Record`, and `Task`, belong to a specific `Tenant`, ensuring data isolation.

### Relationships

-   **User & Tenant**: A many-to-many relationship. A user can be a member of multiple tenants, and a tenant can have multiple users.
-   **Tenant & Resources**: A one-to-many relationship. Each tenant owns multiple persons, tasks, calendar events, records, and tags.
-   **Record & Tag**: A many-to-many relationship. A record can have multiple tags, and a tag can be applied to multiple records.

---

## Models

### `User` Model

Represents a user account in the system.

| Column | Type | Description |
| --- | --- | --- |
| `id` | `String` | Primary key, UUID. |
| `username` | `String` | Unique username for login. |
| `email` | `String` | Unique email address. |
| `full_name` | `String` | The user's full name. |
| `hashed_password` | `String` | The user's hashed password. |
| `is_active` | `Boolean` | Whether the user account is active. Defaults to `True`. |
| `is_superuser`| `Boolean` | Whether the user has superuser privileges. Defaults to `False`. |

**Relationships:**
-   `tenants`: Many-to-many relationship with the `Tenant` model via the `user_tenants` association table.

### `Tenant` Model

Represents a department or organization, which acts as a data silo.

| Column | Type | Description |
| --- | --- | --- |
| `id` | `String` | Primary key, UUID. |
| `name` | `String` | The unique name of the tenant. |
| `description` | `String` | An optional description of the tenant. |

**Relationships:**
-   `users`: Many-to-many with `User`.
-   `persons`, `tasks`, `calendar_events`, `records`, `tags`: One-to-many relationships.

### `Person` Model

Represents an individual's profile within a tenant.

| Column | Type | Description |
| --- | --- | --- |
| `id` | `String` | Primary key, UUID. |
| `tenant_id` | `String` | Foreign key linking to the `Tenant` model. |
| `name` | `String` | The person's name. |
| `date_of_birth` | `Date` | The person's date of birth. |
| `gender` | `Enum` | The person's gender (`MALE`, `FEMALE`, `OTHER`). |
| `contact_info`| `JSON` | A JSON object for storing contact details. |

**Relationships:**
-   `tenant`: Many-to-one relationship with `Tenant`.

### `Record` Model

Represents a case file or record within a tenant.

| Column | Type | Description |
| --- | --- | --- |
| `id` | `String` | Primary key, UUID. |
| `tenant_id` | `String` | Foreign key linking to the `Tenant` model. |
| `title` | `String` | The title of the record. |
| `content` | `Text` | The main content of the record. |
| `created_at` | `DateTime` | Timestamp of when the record was created. |
| `updated_at` | `DateTime` | Timestamp of the last update. |

**Relationships:**
-   `tenant`: Many-to-one relationship with `Tenant`.
-   `tags`: Many-to-many relationship with the `Tag` model via the `record_tags` association table.

### `Tag` Model

Represents a tag that can be applied to records.

| Column | Type | Description |
| --- | --- | --- |
| `id` | `String` | Primary key, UUID. |
| `tenant_id` | `String` | Foreign key linking to the `Tenant` model. |
| `name` | `String` | The unique name of the tag within the tenant. |

**Relationships:**
-   `tenant`: Many-to-one relationship with `Tenant`.
-   `records`: Many-to-many relationship with `Record`.

### Other Models

The `Task` and `Calendar` models follow a similar structure to `Person` and `Record`, each belonging to a single `Tenant`.
