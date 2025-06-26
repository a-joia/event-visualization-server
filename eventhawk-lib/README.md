# EventHawk Client Library

A Python client library for interacting with the Dashboard API. This library provides a clean, type-safe interface for managing events through the backend API.

## Features

- **Type Safety**: Full type hints and data validation
- **Easy to Use**: Simple, intuitive API
- **Comprehensive**: All CRUD operations for events
- **Search & Filter**: Built-in search and filtering capabilities
- **Pagination**: Support for paginated results
- **Error Handling**: Proper exception handling
- **Context Manager**: Support for `with` statements

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Import the library:
   ```python
   from eventhawk_lib import EventHawkClient, EventCreate, EventUpdate
   ```

## Quick Start

```python
from eventhawk_lib import EventHawkClient, EventCreate
from datetime import datetime

# Create a client
client = EventHawkClient("http://localhost:8000")

# Check API health
health = client.health_check()
print(f"API Health: {health}")

# Get all events
events_response = client.get_events(offset=0, limit=10)
print(f"Found {events_response.total} events")

# Create a new event
new_event = EventCreate(
    id=123,
    name="My Event",
    summary="Event summary",
    status="pending",
    tag="test",
    time=datetime.now().isoformat(),
    description="Event description"
)

created_event = client.create_event(new_event)
print(f"Created event: {created_event.name}")

# Close the client
client.close()
```

## API Reference

### EventHawkClient

The main client class for interacting with the API.

#### Constructor

```python
EventHawkClient(base_url: str = "http://localhost:8000")
```

- `base_url`: Base URL of the API server (default: http://localhost:8000)

#### Methods

##### `health_check() -> dict`
Check API health status.

##### `create_event(event: EventCreate) -> Event`
Create a new event.

##### `get_event(event_id: int) -> Event`
Get a single event by ID.

##### `get_events(offset: int = 0, limit: int = 20, search_query: Optional[str] = None) -> EventListResponse`
Get paginated list of events with optional search.

##### `update_event(event_id: int, event_update: EventUpdate) -> Event`
Update an existing event.

##### `delete_event(event_id: int) -> bool`
Delete an event.

##### `search_events(query: str, limit: int = 20) -> List[Event]`
Search for events by query string.

##### `get_events_by_status(status: str, limit: int = 20) -> List[Event]`
Get events filtered by status.

##### `get_events_by_tag(tag: str, limit: int = 20) -> List[Event]`
Get events filtered by tag.

##### `get_recent_events(hours: int = 24, limit: int = 20) -> List[Event]`
Get recent events from the last N hours.

### Data Models

#### Event
```python
@dataclass
class Event:
    id: int
    name: str
    summary: str
    status: str
    tag: str
    time: str
    description: str
```

#### EventCreate
```python
@dataclass
class EventCreate:
    id: int
    name: str
    summary: str
    status: str
    tag: str
    time: str
    description: str
```

#### EventUpdate
```python
@dataclass
class EventUpdate:
    name: Optional[str] = None
    summary: Optional[str] = None
    status: Optional[str] = None
    tag: Optional[str] = None
    time: Optional[str] = None
    description: Optional[str] = None
```

## Usage Examples

### Basic CRUD Operations

```python
from eventhawk_lib import EventHawkClient, EventCreate, EventUpdate
from datetime import datetime

with EventHawkClient("http://localhost:8000") as client:
    # Create
    new_event = EventCreate(
        id=456,
        name="Test Event",
        summary="Test summary",
        status="pending",
        tag="test",
        time=datetime.now().isoformat(),
        description="Test description"
    )
    created = client.create_event(new_event)
    
    # Read
    event = client.get_event(456)
    print(f"Event: {event.name}")
    
    # Update
    update = EventUpdate(status="solved")
    updated = client.update_event(456, update)
    
    # Delete
    client.delete_event(456)
```

### Search and Filter

```python
with EventHawkClient("http://localhost:8000") as client:
    # Search
    results = client.search_events("error", limit=10)
    
    # Filter by status
    pending_events = client.get_events_by_status("pending")
    
    # Filter by tag
    system_events = client.get_events_by_tag("system")
    
    # Get recent events
    recent = client.get_recent_events(hours=24)
```

### Pagination

```python
with EventHawkClient("http://localhost:8000") as client:
    page = 0
    page_size = 10
    
    while True:
        response = client.get_events(offset=page * page_size, limit=page_size)
        
        for event in response.events:
            print(f"Event: {event.name}")
        
        if len(response.events) < page_size:
            break
        
        page += 1
```

## Error Handling

The library provides proper error handling:

```python
try:
    event = client.get_event(999)
except Exception as e:
    print(f"Error: {e}")
    # Handle the error appropriately
```

## Context Manager

The client supports context manager syntax for automatic cleanup:

```python
with EventHawkClient("http://localhost:8000") as client:
    events = client.get_events()
    # Client is automatically closed when exiting the context
```

## Running Examples

To run the included examples:

```bash
cd eventhawk-lib
python examples.py
```

Make sure the backend server is running on `http://localhost:8000` before running the examples.

## Requirements

- Python 3.8+
- requests>=2.25.0

## License

This library is part of the Dashboard project. 