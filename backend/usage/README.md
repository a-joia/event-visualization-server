# Usage Examples

This folder contains practical examples demonstrating how to use different components of the backend system.

## Examples Overview

### 1. `database_manager_example.py`
**Purpose**: Demonstrates direct usage of the DatabaseManager class
**What it shows**:
- Database initialization
- CRUD operations (Create, Read, Update, Delete)
- Filtering and searching
- Record counting
- Error handling

**Run with**:
```bash
cd backend
python usage/database_manager_example.py
```

### 2. `service_example.py`
**Purpose**: Shows how to use the EventService class for business logic
**What it shows**:
- Service layer operations
- Event creation, retrieval, updates, and deletion
- Pagination and searching
- Status and tag filtering
- Statistics gathering

**Run with**:
```bash
cd backend
python usage/service_example.py
```

### 3. `api_example.py`
**Purpose**: Demonstrates API endpoint usage via HTTP requests
**What it shows**:
- HTTP API interactions
- RESTful operations
- Response handling
- Error management
- Real-world API testing

**Prerequisites**: Backend server must be running
**Run with**:
```bash
# First start the backend server
cd backend
python main.py

# Then in another terminal
cd backend
python usage/api_example.py
```

### 4. `event_times_example.py`
**Purpose**: Demonstrates the new event_start and event_end fields
**What it shows**:
- Working with event time ranges
- Filtering events by time periods
- Duration calculations
- Finding events happening at specific times
- Upcoming event detection

**Run with**:
```bash
cd backend
python usage/event_times_example.py
```

## Running the Examples

### Prerequisites
1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. For API examples, ensure the backend server is running:
   ```bash
   python main.py
   ```

### Execution Order
For a complete demonstration, run the examples in this order:

1. **Database Manager Example** (direct database operations)
2. **Service Example** (business logic layer)
3. **API Example** (HTTP interface)

### Expected Output
Each example will:
- ✅ Show successful operations
- ❌ Display any errors encountered
- 📊 Provide statistics and counts
- 🔍 Demonstrate search and filtering capabilities

## Example Output

```
=== DatabaseManager Example Usage ===

1. Initializing database...
✅ Database initialized successfully!

2. Writing sample events to database...
✅ Sample events inserted successfully!

3. Reading events from database...
📊 Found 3 events:
   - ID: 1, Name: System Startup, Status: completed
   - ID: 2, Name: User Login, Status: active
   - ID: 3, Name: Data Export, Status: completed

=== Example completed successfully! ===
```

## Customization

You can modify these examples to:
- Test different data scenarios
- Add new operations
- Experiment with different filters and searches
- Test error conditions
- Benchmark performance

## Troubleshooting

### Import Errors
If you get import errors, ensure you're running from the correct directory:
```bash
cd backend
python usage/example_name.py
```

### Database Errors
- Ensure the database file is writable
- Check that all dependencies are installed
- Verify the database URL in `config.py`

### API Connection Errors
- Make sure the backend server is running on `http://localhost:8000`
- Check that the server started without errors
- Verify the API endpoints are accessible

## Next Steps

After running these examples, you can:
1. Explore the actual code to understand the implementation
2. Modify the examples for your specific use cases
3. Create your own examples for new features
4. Use these patterns in your own applications 