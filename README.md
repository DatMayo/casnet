# 🚀 Casnet Backend API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.118.0-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square&logo=python)](https://python.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.11+-e92063?style=flat-square)](https://pydantic.dev/)

> **Enterprise-Grade Multi-Tenant Backend API** - Production-ready with comprehensive security, monitoring, and developer experience features.

A high-performance FastAPI-based backend application designed for **roleplay servers** and departmental management systems. Features a complete suite of CRUD API endpoints with advanced security, multi-tenant isolation, comprehensive validation, and enterprise monitoring capabilities.


## ✨ Key Features

- 🏢 **Multi-Tenant Architecture** - Complete data isolation between departments
- 🛡️ **Enterprise Security** - JWT authentication, input validation, request limiting  
- 📊 **Rich API Documentation** - Auto-generated with comprehensive parameter descriptions
- 🔄 **Pagination Support** - Frontend-ready with metadata for UI components
- 🏥 **Health Monitoring** - Kubernetes-compatible readiness/liveness probes
- 💾 **Persistent Database** - Uses SQLite by default for reliable data storage.
- 🚀 **SQLAlchemy 2.0** - Modern, fully-typed data models and queries.
- 🐳 **Docker Ready** - Includes `Dockerfile` and `docker-compose.yml` for easy containerization.
- ⚡ **High Performance** - Asynchronous and built for speed.
- 🌐 **CORS Ready** - Configured for all major frontend frameworks.
- 🎯 **Developer Experience** - Structured errors, comprehensive logging, hot reload.

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

## 🔗 API Endpoints

### Core Resources
Full CRUD operations with pagination are available for all core resources. For a complete list of endpoints, parameters, and request/response examples, please see the **[Interactive API Documentation](#-api-documentation)**.

- **Authentication**: `POST /token`
- **Users**: `/user`
- **Tenants**: `/tenant`
- **Persons**: `/person/{tenant_id}`
- **Tasks**: `/task/{tenant_id}`
- **Calendar Events**: `/calendar/{tenant_id}`
- **Records**: `/record/{tenant_id}`
- **Tags**: `/tag/{tenant_id}`

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
git clone <repository-url>
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
   git clone <repository-url>
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

# Development Settings
DATA_COUNT=10
ENABLE_DETAILED_LOGGING=true
ENVIRONMENT=development

# API Configuration
API_TITLE=Casnet Backend API
API_VERSION=1.0.0

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

### Authentication & Authorization  
- **JWT-based authentication** with configurable expiration
- **Password hashing** using bcrypt
- **Role-based access control** within tenant boundaries

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

All list endpoints return paginated results with comprehensive metadata:

```json
{
  "data": [...],
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

### Adding New Endpoints
1.  **Model**: Create or update a SQLAlchemy model in `src/models/`.
2.  **Schema**: Define Pydantic validation schemas in `src/schemas/`.
3.  **Router**: Add a new router file with CRUD endpoints in `src/routers/`.
4.  **Main**: Include the new router in `src/main.py`.

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
git clone <repository-url>
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

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎯 What's Next?

This project now serves as a robust foundation for any multi-tenant application. Recommended next steps include:

- **Frontend Development**: The API is ready for integration with any modern frontend framework (React, Vue, Angular, etc.).
- **Implement Caching**: Integrate Redis (already available in Docker) for response caching to improve performance.
- **Add Rate Limiting**: Implement request rate limiting to protect against abuse.
- **File Uploads**: Extend the API to support file uploads for records or user profiles.
