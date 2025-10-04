# 🚀 Casnet Backend API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.118.0-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square&logo=python)](https://python.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.11+-e92063?style=flat-square)](https://pydantic.dev/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/DatMayo/casnet-backend?style=flat-square)](https://github.com/DatMayo/casnet-backend/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/DatMayo/casnet-backend?style=flat-square)](https://github.com/DatMayo/casnet-backend/commits/main)

> **Enterprise-Grade Multi-Tenant Backend API** - Production-ready with comprehensive security, monitoring, and developer experience features.

A high-performance FastAPI-based backend application designed for **roleplay servers** and departmental management systems. Features a complete suite of CRUD API endpoints with advanced security, multi-tenant isolation, comprehensive validation, and enterprise monitoring capabilities.


## ✨ Key Features

- 🏢 **Multi-Tenant Architecture** - Complete data isolation between departments with smart defaults
- 🛡️ **Enterprise Security** - Complete JWT auth lifecycle (login/logout/refresh) with automatic tenant filtering
- 📊 **Modern RESTful API** - Clean plural endpoints (`/users`, `/persons`) with consistent patterns
- 🔄 **Enhanced UX** - Simplified URLs, automatic tenant access, no complex tenant_id parameters
- 🏥 **Health Monitoring** - Kubernetes-compatible readiness/liveness probes
- 💾 **Persistent Database** - Uses SQLite by default, production-safe initialization
- 🚀 **SQLAlchemy 2.0** - Modern, fully-typed data models and queries
- 🐳 **Docker Ready** - Includes `Dockerfile` and `docker-compose.yml` for easy containerization
- ⚡ **High Performance** - Asynchronous and built for speed
- 🌐 **CORS Ready** - Configured for all major frontend frameworks
- 🎯 **Developer Experience** - Auto-generated docs, structured errors, hot reload, immediate testing

## 🏗️ Project Structure

```
casnet-backend/
├── src/                    # Application source code
│   ├── enum/               # Enumerations (EStatus, EGender)
│   ├── models/             # SQLAlchemy 2.0 database models
│   ├── schemas/            # Pydantic data validation schemas
│   ├── routers/            # API endpoint definitions
│   ├── config.py           # Environment configuration
│   ├── database.py         # Database session and initialization
│   ├── exceptions.py       # Custom exception classes
│   ├── hashing.py          # Password hashing utilities
│   ├── main.py             # FastAPI application entry point
│   ├── security.py         # JWT & authentication utilities
│   ├── util.py             # General helper functions
│   └── validation.py       # Input validation & sanitization
├── data/
│   └── casnet.db           # SQLite database file (gitignored)
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Development environment
├── .dockerignore           # Docker ignore patterns
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 📚 Documentation

### 🌟 **Comprehensive Wiki Available**
For detailed guides, tutorials, and in-depth documentation, visit our **[GitHub Wiki](https://github.com/DatMayo/casnet-backend/wiki)**:

- **📖 [Getting Started Guide](https://github.com/DatMayo/casnet-backend/wiki/Home)** - Project overview and quick start
- **🐳 [Docker Quickstart](https://github.com/DatMayo/casnet-backend/wiki/Docker-Quickstart)** - Fast Docker setup guide
- **🛠️ [Local Development Setup](https://github.com/DatMayo/casnet-backend/wiki/Local-Development-Setup)** - Python development environment
- **🏗️ [Multi-Tenant Architecture](https://github.com/DatMayo/casnet-backend/wiki/Multi-Tenant-Architecture)** - System design and data isolation
- **🗄️ [Database Schema](https://github.com/DatMayo/casnet-backend/wiki/Database-Schema)** - SQLAlchemy models and relationships
- **🚀 [Deployment Guide](https://github.com/DatMayo/casnet-backend/wiki/Deployment-Guide)** - Production deployment strategies
- **🔒 [Authentication Flow](https://github.com/DatMayo/casnet-backend/wiki/Authentication-Flow)** - JWT security implementation

> 💡 **Tip**: The wiki is constantly updated with new examples, troubleshooting guides, and advanced use cases.

### 📖 API Documentation
**Interactive Docs** (when running):
- **Swagger UI**: [`http://localhost:8000/docs`](http://localhost:8000/docs) 
- **ReDoc**: [`http://localhost:8000/redoc`](http://localhost:8000/redoc)
- **Health Check**: [`http://localhost:8000/health`](http://localhost:8000/health)

**Detailed Guides** (GitHub Wiki):
- **🔐 [Authentication](https://github.com/DatMayo/casnet-backend/wiki/API-Authentication)** - JWT tokens and security
- **👥 [Users API](https://github.com/DatMayo/casnet-backend/wiki/API-Users)** - User management endpoints
- **🏢 [Tenants API](https://github.com/DatMayo/casnet-backend/wiki/API-Tenants)** - Multi-tenant organization
- **👤 [Persons API](https://github.com/DatMayo/casnet-backend/wiki/API-Persons)** - Individual profiles
- **📋 [Tasks & Calendar API](https://github.com/DatMayo/casnet-backend/wiki/API-Tasks-and-Calendar)** - Task and event management
- **📄 [Records & Tags API](https://github.com/DatMayo/casnet-backend/wiki/API-Records-and-Tags)** - Document and categorization

## 🔗 API Endpoints

### 🔐 Authentication
- `POST /auth/login` - User authentication and token generation
- `POST /auth/logout` - User logout (client-side cleanup)
- `POST /auth/refresh` - Token refresh to extend session
- `GET /auth/me` - Get current user profile and accessible tenants

### 🏢 Core Resources
Full CRUD operations with pagination are available for all core resources. All endpoints automatically filter data based on the user's accessible tenants for enhanced security and simplified access.

#### **RESTful Endpoint Structure**
```
GET    /users?tenant_id=xyz    # List users from specific tenant (paginated)
POST   /users                  # Create new user
GET    /users/{id}             # Get specific user
PUT    /users/{id}             # Update user
DELETE /users/{id}             # Delete user

GET    /tenants                # List user's accessible tenants
POST   /tenants                # Create new tenant  
GET    /tenants/{id}           # Get specific tenant
PUT    /tenants/{id}           # Update tenant
DELETE /tenants/{id}           # Delete tenant

GET    /persons?tenant_id=xyz  # List persons from specific tenant (paginated)
POST   /persons?tenant_id=xyz  # Create person in specific tenant
GET    /persons/{id}           # Get specific person (auto-searches user's tenants)
PUT    /persons/{id}           # Update person
DELETE /persons/{id}           # Delete person

GET    /tasks?tenant_id=xyz    # List tasks from specific tenant (paginated)
POST   /tasks?tenant_id=xyz    # Create task in specific tenant
GET    /tasks/{id}             # Get specific task
PUT    /tasks/{id}             # Update task
DELETE /tasks/{id}             # Delete task

GET    /records?tenant_id=xyz  # List records from specific tenant (paginated)
POST   /records?tenant_id=xyz  # Create record in specific tenant
GET    /records/{id}           # Get specific record
PUT    /records/{id}           # Update record
DELETE /records/{id}           # Delete record

GET    /tags?tenant_id=xyz     # List tags from specific tenant (paginated)
POST   /tags?tenant_id=xyz     # Create tag in specific tenant
GET    /tags/{id}              # Get specific tag
PUT    /tags/{id}              # Update tag
DELETE /tags/{id}              # Delete tag
```

#### **Key Improvements**
- ✅ **Consistent plural naming** - All resources use plural forms (`/users`, `/persons`, etc.)
- ✅ **Clean URLs** - No more complex `/{tenant_id}/{resource_id}` paths in routes
- ✅ **Flexible tenant filtering** - List endpoints use query parameters for tenant-specific data
- ✅ **RESTful design** - Follows modern API design patterns with proper HTTP methods
- ✅ **Enhanced security** - Tenant access automatically validated on all endpoints
- ✅ **Hybrid approach** - Clean URLs with optional tenant-specific filtering when needed

### 🏥 Health & Monitoring
- `GET /health` - Basic health check
- `GET /health/detailed` - Comprehensive metrics & uptime
- `GET /health/ready` - Kubernetes readiness probe
- `GET /health/live` - Kubernetes liveness probe

### 📖 API Documentation
- `GET /docs` - Interactive Swagger UI documentation
- `GET /redoc` - Alternative ReDoc documentation
- `GET /openapi.json` - OpenAPI schema

## 🚀 Getting Started

### 🐳 **Recommended: Docker Setup (5-minute setup)**

```bash
# Clone the repository
git clone https://github.com/DatMayo/casnet-backend.git
cd casnet-backend

# Start the FastAPI development server
docker-compose up -d casnet-api

# Access the interactive API documentation
open http://localhost:8000/docs

# View live server logs (optional)
docker-compose logs -f casnet-api
```

**✅ What you get:**
- FastAPI server with **hot reload** (code changes auto-restart)
- **Health monitoring** at `http://localhost:8000/health`
- **Interactive API docs** at `http://localhost:8000/docs`
- **All enterprise features** enabled (validation, pagination, etc.)

### 🐍 Alternative: Local Python Setup

1. **Clone & Setup Virtual Environment**
   ```bash
   git clone https://github.com/DatMayo/casnet-backend.git
   cd casnet-backend
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   uvicorn src.main:app --reload
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Security Settings
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=sqlite:///./data/casnet.db
DATABASE_ECHO=false

# Development Settings
DATA_COUNT=10
ENABLE_DETAILED_LOGGING=true
ENVIRONMENT=development

# Documentation Settings (set to false in production for security)
ENABLE_DOCS=true
ENABLE_REDOC=true

# API Configuration
API_TITLE=Casnet Backend API
API_VERSION=1.0.0
API_PREFIX=/api/v1

# CORS Settings (for frontend development)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Security & Input Validation
MAX_REQUEST_SIZE=16777216
MAX_STRING_LENGTH=1000
MAX_DESCRIPTION_LENGTH=5000
```

### Key Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./data/casnet.db` | Database connection string |
| `DATA_COUNT` | `10` | Number of dummy records to generate on first run |
| `MAX_REQUEST_SIZE` | `16777216` | Maximum request size in bytes (16MB) |
| `MAX_STRING_LENGTH` | `1000` | Maximum length for string fields |
| `ALLOWED_ORIGINS` | Development URLs | CORS allowed origins |

## 🛡️ Security Features

### Multi-Tenant Architecture
- **Complete data isolation** between tenants
- **Tenant-scoped API access** - users can only access data from their assigned tenants
- **Automatic tenant validation** on all endpoints
- **Smart defaults** - automatically creates default admin user and "Default Organization" tenant on first run
- **Production-safe** - only creates defaults when database is completely empty

### Authentication & Authorization  
- **JWT-based authentication** with configurable expiration and refresh tokens
- **Password hashing** using bcrypt with secure salt rounds
- **Role-based access control** within tenant boundaries
- **Complete auth lifecycle** - login, logout, token refresh, and profile access
- **Automatic tenant validation** - users can only access their assigned tenant data

### Input Validation & Security
- **Request size limiting** - prevents DoS attacks via large payloads
- **Comprehensive input validation** - sanitizes and validates all user input
- **Structured error responses** - detailed validation feedback
- **CORS protection** - configurable cross-origin resource sharing

### Example Security Responses

**Validation Error:**
```json
{
  "error_code": "VALIDATION_FAILED",
  "message": "Field 'name' contains invalid characters", 
  "field_errors": [
    {
      "field": "name",
      "message": "Only letters, numbers, spaces, hyphens, and underscores allowed",
      "invalid_value": "invalid<script>"
    }
  ]
}
```

**Request Too Large:**
```json
{
  "error_code": "REQUEST_TOO_LARGE",
  "message": "Request body too large. Maximum size: 16777216 bytes"
}
```

## 📊 Pagination

All list endpoints return paginated results with comprehensive metadata. The API uses a consistent `data`/`meta` structure:

```json
{
  "data": [
    {
      "id": "person_123",
      "name": "John Doe",
      "tenant_id": "tenant_xyz"
    }
  ],
  "meta": {
    "total_items": 150,
    "total_pages": 8, 
    "current_page": 2,
    "page_size": 20,
    "has_next": true,
    "has_previous": true,
    "next_page": 3,
    "previous_page": 1
  }
}
```

### Pagination Parameters
- `page` - Page number (1-indexed, default: 1)  
- `page_size` - Items per page (default: 20, max: 100)
- `tenant_id` - Required for list endpoints to specify which tenant's data to retrieve

## 🏥 Health Monitoring

### Health Check Endpoints

- **`/health`** - Basic health status
- **`/health/detailed`** - Comprehensive metrics including uptime and configuration
- **`/health/ready`** - Readiness probe for deployment systems  
- **`/health/live`** - Liveness probe for container orchestration

### Example Health Response
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "version": "1.0.0",
  "environment": "development",
  "uptime_seconds": 3600,
  "data_status": {
    "tenants_loaded": 25,
    "users_loaded": 10
  }
}
```

## 🔄 Development Workflow

### Hot Reload
The development server supports hot reload - changes to source files automatically restart the server.

### API Testing
Use the interactive documentation at `/docs` to test endpoints directly in your browser.

### Quick Start Testing
After starting the server, you can immediately test the API:

1. **Get Auth Token**: POST to `/auth/login` with `admin/changeme`
2. **Test Profile**: GET `/auth/me` to see your user profile and accessible tenants
3. **Get Tenant ID**: Note the tenant ID from the `/auth/me` response (e.g., "Default Organization")
4. **List Resources**: GET `/persons?tenant_id=xyz`, `/tasks?tenant_id=xyz`, etc. using your tenant ID
5. **Create Data**: POST to any resource endpoint with `tenant_id` as query parameter
6. **Individual Access**: GET `/persons/{id}`, `/tasks/{id}` (auto-searches across accessible tenants)

### Enhanced Developer Experience
- **Automatic defaults** - No setup required, default admin and tenant created automatically
- **RESTful URLs** - Clean, predictable endpoint structure with query parameter filtering
- **Comprehensive errors** - Detailed validation feedback and clear error messages
- **Flexible tenant access** - Use query parameters for lists, individual IDs work across tenants
- **Modern patterns** - Follows REST conventions with proper HTTP methods and status codes
- **Hybrid approach** - Balance between simplicity and tenant-specific control

### Adding New Endpoints
1.  **Model**: Create or update a SQLAlchemy model in `src/models/`.
2.  **Schema**: Define Pydantic validation schemas in `src/schemas/`.
3.  **Router**: Add a new router file with CRUD endpoints in `src/routers/`.
4.  **Main**: Include the new router in `src/main.py`.
5.  **Follow patterns**: Use plural resource names and implement tenant filtering like existing routers.

## ⚙️ Database

This application uses **SQLAlchemy 2.0** for its ORM and comes pre-configured to use a **persistent SQLite database**. 

- The database file is located at `data/casnet.db`.
- The `data/` directory is automatically created and is included in `.gitignore`.

### Migrating to PostgreSQL
For a more robust production environment, you can switch to PostgreSQL:
1.  Update the `DATABASE_URL` in your `.env` file:
    ```env
    DATABASE_URL=postgresql://username:password@localhost:5432/casnet
    ```
2.  Install the PostgreSQL driver:
    ```bash
    pip install psycopg2-binary
    ```
3.  Restart the application.

## 🐳 Docker Support

### Quick Start with Docker

**🚀 Recommended: Start with Docker (Easiest) - ✅ Verified Working**
```bash
# Clone and start the development environment
git clone https://github.com/DatMayo/casnet-backend.git
cd casnet-backend

# Start the FastAPI container (API only)
docker-compose up -d casnet-api

# View logs
docker-compose logs -f casnet-api

# Access the API
open http://localhost:8000/docs
```

**🏗️ Full Stack with Database (Optional)**
```bash
# Start with PostgreSQL and Redis for database migration testing
docker-compose --profile full-stack up -d

# Stop services
docker-compose down
```

### Docker Configuration

#### **Development Stack (`docker-compose.yml`)**
- **FastAPI**: Development server with hot reload on port 8000
- **PostgreSQL**: Optional database service (profile: `full-stack`)
- **Redis**: Optional caching service (profile: `full-stack`)

#### **Services Overview**

| Service | Port | Status | Purpose |
|---------|------|--------|---------|
| FastAPI API | `8000` | ✅ Running | Main backend application |
| PostgreSQL | `5432` | 🔧 Optional | Database (future migration) |
| Redis | `6379` | 🔧 Optional | Caching & rate limiting |

### Docker Commands

```bash
# Basic operations
docker-compose up -d casnet-api         # Start API only
docker-compose up -d                    # Start API only (same as above)
docker-compose --profile full-stack up -d # Start with database
docker-compose ps                       # Check container status
docker-compose logs -f casnet-api       # View live logs
docker-compose down                     # Stop all services

# Development helpers
docker-compose exec casnet-api bash     # Access container shell
docker-compose restart casnet-api       # Restart API container
```

### Container Features

#### **✅ Production-Ready Features:**
- **Multi-stage builds** for development and production
- **Health checks** built into containers
- **Hot reload** support for development
- **Non-root user** in production containers
- **Optimized build caching** with .dockerignore

#### **🔧 Current Status:**
- **✅ FastAPI Container**: Working perfectly with hot reload
- **✅ Health Monitoring**: Container reports healthy status  
- **✅ Port Mapping**: Correctly exposed on localhost:8000
- **✅ Interactive Docs**: Available at http://localhost:8000/docs
- **✅ OpenAPI Schema**: Comprehensive API documentation automatically generated.
- **🔧 Database**: PostgreSQL container is available but requires the `full-stack` profile to be activated.

## 🚀 Deployment

### Environment Setup
- **Development**: Use Docker Compose (recommended) or local Python setup
- **Production**: Use production Docker containers with secrets management
- **Staging**: Separate compose files for staging environment

### Health Checks & Monitoring
- **Docker**: Built-in health checks for all services
- **Kubernetes**: Compatible readiness/liveness probes at `/health`
- **Load Balancer**: Health endpoints ready for production deployment

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Read the Documentation**: Check our **[Local Development Setup](https://github.com/DatMayo/casnet-backend/wiki/Local-Development-Setup)** and **[Contributing Guide](https://github.com/DatMayo/casnet-backend/wiki/Contributing-to-the-Wiki)** in the wiki
2. Fork the repository
3. Create a feature branch (`git checkout -b feature/amazing-feature`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

For detailed contribution guidelines, coding standards, and development setup, visit our **[GitHub Wiki](https://github.com/DatMayo/casnet-backend/wiki)**.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎯 What's Next?

This project now serves as a robust foundation for any multi-tenant application. Recommended next steps include:

- **Frontend Development**: The API is ready for integration with any modern frontend framework (React, Vue, Angular, etc.).
- **Implement Caching**: Integrate Redis (already available in Docker) for response caching to improve performance.
- **Add Rate Limiting**: Implement request rate limiting to protect against abuse.
- **File Uploads**: Extend the API to support file uploads for records or user profiles.
