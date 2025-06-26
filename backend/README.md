# Dashboard Backend API

A FastAPI-based backend for the dashboard application with organized, maintainable code structure.

## Project Structure

```
backend/
├── apis/                 # API route handlers
│   └── events.py        # Event-related API endpoints
├── config.py            # Application configuration
├── database.py          # Database setup and session management
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for request/response validation
├── services.py          # Business logic layer
├── main.py              # FastAPI application entry point
├── init_db.py           # Database initialization script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Architecture

The backend follows a clean architecture pattern with clear separation of concerns:

### Layers

1. **API Layer** (`apis/`) - Route handlers and HTTP request/response handling
2. **Service Layer** (`services.py`) - Business logic and database operations
3. **Data Layer** (`models.py`, `database.py`) - Database models and connection management
4. **Schema Layer** (`schemas.py`) - Data validation and serialization

### Key Features

- **Async/Await**: Full async support with SQLAlchemy async
- **Dependency Injection**: FastAPI dependency injection for database sessions
- **Type Safety**: Comprehensive type hints throughout
- **Validation**: Pydantic schemas for request/response validation
- **Error Handling**: Proper HTTP status codes and error messages
- **Documentation**: Auto-generated API documentation with FastAPI

## API Endpoints

### Events

- `POST /api/events` - Create a new event
- `GET /api/events` - Get paginated list of events (with search)
- `GET /api/events/{event_id}` - Get a specific event
- `PUT /api/events/{event_id}` - Update an event
- `DELETE /api/events/{event_id}` - Delete an event

### Health Check

- `GET /api/health` - Health check endpoint
- `GET /` - Root endpoint with API information

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize the database:
   ```bash
   python init_db.py
   ```

3. Start the development server:
   ```bash
   python main.py
   ```

   Or with uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

4. Access the API:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/api/health

## Configuration

All configuration is centralized in `config.py`. Key settings include:

- Database URL
- CORS settings
- API metadata
- Pagination limits

## Development

### Adding New Models

1. Add the model to `models.py`
2. Create corresponding schemas in `schemas.py`
3. Add business logic to `services.py`
4. Create API endpoints in `apis/`

### Database Migrations

For production, consider using Alembic for database migrations.

## Testing

The API includes comprehensive error handling and validation. Test endpoints using:

- FastAPI's auto-generated documentation at `/docs`
- curl commands
- Postman or similar API testing tools

## Production Deployment

For production deployment:

1. Set up proper environment variables
2. Configure CORS origins properly
3. Use a production ASGI server (Gunicorn + Uvicorn)
4. Set up proper logging
5. Consider using a production database (PostgreSQL, MySQL)

## Database Backend Abstraction

All database engine, session, and base management is now centralized in `db_provider.py`. To switch to a different database backend (e.g., PostgreSQL, MySQL), update the `DATABASE_URL` in `config.py` and, if needed, adjust the engine/session logic in `db_provider.py`. The rest of the app does not need to change.

- Use `Base` from `db_provider.py` for model definitions
- Use `get_db` as a FastAPI dependency
- Use `init_db` for migrations or startup

Example:
```python
from db_provider import engine, AsyncSessionLocal, Base, get_db, init_db
```

## DatabaseManager Class

The `DatabaseManager` class provides a clean, abstracted interface for all database operations. This makes it easy to switch between different database backends and provides a consistent API for data access.

### Key Features

- **Backend Agnostic**: Easy to switch between SQLite, PostgreSQL, MySQL, etc.
- **Simple Interface**: Three main methods: `init_database()`, `get_from_database()`, `write_to_database()`
- **Built-in Logging**: Comprehensive error handling and logging
- **Type Safety**: Full type hints and validation

### Main Methods

#### `init_database()`
Initialize the database and create all tables.

```python
from database_manager import db_manager

success = await db_manager.init_database()
if success:
    print("Database initialized successfully!")
```

#### `get_from_database(table_name, filters=None, limit=None, offset=None, order_by=None, search_query=None)`
Retrieve data from the database with optional filtering, pagination, and search.

```python
# Get all events
events = await db_manager.get_from_database(
    table_name="events",
    limit=10,
    order_by="id"
)

# Get events with filter
active_events = await db_manager.get_from_database(
    table_name="events",
    filters={"status": "active"}
)

# Search events
search_results = await db_manager.get_from_database(
    table_name="events",
    search_query="export",
    limit=5
)
```

#### `write_to_database(table_name, data, operation="insert")`
Write data to the database. Supports insert, update, and delete operations.

```python
# Insert new records
success = await db_manager.write_to_database(
    table_name="events",
    data={"id": 1, "name": "Test Event", "status": "active"},
    operation="insert"
)

# Update existing record
success = await db_manager.write_to_database(
    table_name="events",
    data={"id": 1, "status": "completed"},
    operation="update"
)

# Delete record
success = await db_manager.write_to_database(
    table_name="events",
    data={"id": 1},
    operation="delete"
)
```

### Additional Methods

#### `count_records(table_name, filters=None)`
Count records in a table with optional filters.

```python
total_count = await db_manager.count_records(table_name="events")
active_count = await db_manager.count_records(
    table_name="events",
    filters={"status": "active"}
)
```

### Example Usage

See the `usage/` folder for complete demonstrations of all DatabaseManager features:

- `usage/database_manager_example.py` - Direct DatabaseManager usage
- `usage/service_example.py` - EventService usage
- `usage/api_example.py` - API endpoint testing

### Switching Database Backends

To switch to a different database backend:

1. **Update the DATABASE_URL in `config.py`**:
   ```python
   # SQLite
   DATABASE_URL = "sqlite+aiosqlite:///events.db"
   
   # PostgreSQL
   DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
   
   # MySQL
   DATABASE_URL = "mysql+aiomysql://user:password@localhost/dbname"
   ```

2. **Install the required driver**:
   ```bash
   # For PostgreSQL
   pip install asyncpg
   
   # For MySQL
   pip install aiomysql
   ```

3. **The rest of your application remains unchanged!**

### Architecture Benefits

- **Separation of Concerns**: Database logic is isolated in one place
- **Testability**: Easy to mock database operations for testing
- **Maintainability**: Single point of change for database operations
- **Extensibility**: Easy to add new database backends or features 