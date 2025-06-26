# How to Edit Event Structure

This guide explains how to modify the event structure in the dashboard application, including database models, API schemas, and frontend integration.

## Current Event Structure

The event structure currently has these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | Integer | Yes | Primary key, auto-generated |
| `name` | String | Yes | Event name |
| `summary` | String | Yes | Brief event summary |
| `status` | String | Yes | Event status |
| `tag` | String | Yes | Event tag/category |
| `time` | String | Yes | Event timestamp |
| `description` | Text | Yes | Detailed event description |

## Ways to Edit Event Structure

### 1. Add New Fields

To add new fields to the event structure, you need to modify several files:

#### Step 1: Update Database Model (`backend/models.py`)

```python
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

class Event(Base):
    """Database model for events"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    status = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    time = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    # New fields example:
    priority = Column(String, nullable=True)
    category = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### Step 2: Update Pydantic Schemas (`backend/schemas.py`)

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class EventBase(BaseModel):
    """Base schema for event data"""
    name: str
    summary: str
    status: str
    tag: str
    time: str
    description: str
    
    # New fields:
    priority: Optional[str] = None
    category: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class EventCreate(EventBase):
    """Schema for creating a new event"""
    id: int

class EventUpdate(BaseModel):
    """Schema for updating an event"""
    name: Optional[str] = None
    summary: Optional[str] = None
    status: Optional[str] = None
    tag: Optional[str] = None
    time: Optional[str] = None
    description: Optional[str] = None
    
    # New fields:
    priority: Optional[str] = None
    category: Optional[str] = None
```

#### Step 3: Database Migration

Since the application uses SQLite, you have two options:

**Option A: Recreate Database (Recommended for development)**
```bash
# Delete existing database
rm backend/events.db

# Run initialization script
cd backend
python init_db.py
```

**Option B: Manual SQL Migration**
```sql
-- Connect to SQLite database and run:
ALTER TABLE events ADD COLUMN priority TEXT;
ALTER TABLE events ADD COLUMN category TEXT;
ALTER TABLE events ADD COLUMN created_at DATETIME;
ALTER TABLE events ADD COLUMN updated_at DATETIME;
```

### 2. Modify Existing Fields

You can change field types, constraints, or add validation:

#### Example: Change Time Field to DateTime

```python
# In models.py
from datetime import datetime

class Event(Base):
    # ... other fields ...
    time = Column(DateTime, nullable=False, default=datetime.utcnow)

# In schemas.py
class EventBase(BaseModel):
    # ... other fields ...
    time: datetime
```

#### Example: Add Field Validation

```python
from pydantic import BaseModel, Field, validator

class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    status: str = Field(..., regex="^(active|inactive|pending)$")
    priority: str = Field(None, regex="^(low|medium|high)$")
    
    @validator('name')
    def name_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
```

### 3. Update API Endpoints

The API endpoints in `backend/apis/events.py` will automatically work with updated schemas, but you may want to add validation or business logic:

```python
@router.post("/events", response_model=EventResponse, status_code=201)
async def create_event(
    event: EventCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new event with validation"""
    # Add custom validation logic here
    if event.priority and event.priority not in ['low', 'medium', 'high']:
        raise HTTPException(status_code=400, detail="Invalid priority value")
    
    service = EventService(db)
    return await service.create_event(event)
```

### 4. Update Frontend Components

After modifying the backend, update the frontend to handle new fields:

#### Update Event Analysis Page (`frontend/src/pages/EventAnalysisPage.jsx`)

```jsx
// Add new form fields
const [formData, setFormData] = useState({
  name: '',
  summary: '',
  status: '',
  tag: '',
  time: '',
  description: '',
  priority: 'medium', // New field
  category: '' // New field
});

// Add form inputs
<div className="mb-4">
  <label className="block text-sm font-medium text-gray-700">Priority</label>
  <select
    value={formData.priority}
    onChange={(e) => setFormData({...formData, priority: e.target.value})}
    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
  >
    <option value="low">Low</option>
    <option value="medium">Medium</option>
    <option value="high">High</option>
  </select>
</div>
```

#### Update Dashboard Widgets (`frontend/src/components/DashboardWidgets.jsx`)

```jsx
// Display new fields in event cards
<div className="event-card">
  <h3>{event.name}</h3>
  <p>{event.summary}</p>
  <div className="event-meta">
    <span className="status">{event.status}</span>
    <span className="priority">{event.priority}</span> {/* New field */}
    <span className="category">{event.category}</span> {/* New field */}
  </div>
</div>
```

### 5. Update Client Library

Update the Python client library in `eventhawk-lib/`:

#### Update Models (`eventhawk-lib/models.py`)

```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Event:
    id: int
    name: str
    summary: str
    status: str
    tag: str
    time: str
    description: str
    priority: Optional[str] = None  # New field
    category: Optional[str] = None  # New field
    created_at: Optional[datetime] = None  # New field
```

#### Update Client Methods (`eventhawk-lib/client.py`)

```python
def create_event(self, name: str, summary: str, status: str, tag: str, 
                time: str, description: str, priority: str = None, 
                category: str = None) -> Event:
    """Create a new event with optional priority and category"""
    event_data = {
        "id": self._get_next_id(),
        "name": name,
        "summary": summary,
        "status": status,
        "tag": tag,
        "time": time,
        "description": description,
        "priority": priority,
        "category": category
    }
    # ... rest of method
```

## Complete Example: Adding Priority Field

Here's a step-by-step example of adding a `priority` field:

### 1. Update Database Model

```python
# backend/models.py
class Event(Base):
    # ... existing fields ...
    priority = Column(String, nullable=True)
```

### 2. Update Schemas

```python
# backend/schemas.py
class EventBase(BaseModel):
    # ... existing fields ...
    priority: Optional[str] = None

class EventUpdate(BaseModel):
    # ... existing fields ...
    priority: Optional[str] = None
```

### 3. Recreate Database

```bash
cd backend
rm events.db
python init_db.py
```

### 4. Update Frontend

Add priority field to forms and displays in React components.

### 5. Update Client Library

Add priority field to Event model and client methods.

### 6. Test Changes

```bash
# Test backend
cd backend
uvicorn main:app --reload

# Test client library
cd ../eventhawk-lib
python examples.py
```

## Best Practices

1. **Backup Data**: Always backup your database before making structural changes
2. **Test Incrementally**: Test each layer (database, API, frontend) separately
3. **Use Migrations**: For production, use proper database migration tools
4. **Validate Data**: Add validation rules for new fields
5. **Update Documentation**: Keep this guide updated with new changes
6. **Version Control**: Commit changes incrementally with clear commit messages

## Common Field Types

| SQLAlchemy Type | Pydantic Type | Description |
|-----------------|---------------|-------------|
| `String` | `str` | Text field with length limit |
| `Text` | `str` | Long text field |
| `Integer` | `int` | Whole number |
| `Float` | `float` | Decimal number |
| `Boolean` | `bool` | True/False value |
| `DateTime` | `datetime` | Date and time |
| `Date` | `date` | Date only |
| `JSON` | `dict` | JSON data |

## Troubleshooting

### Common Issues

1. **Database Schema Mismatch**: Delete `events.db` and recreate
2. **Pydantic Validation Errors**: Check field types and validation rules
3. **Frontend Form Errors**: Ensure form field names match backend schema
4. **API 422 Errors**: Verify request body matches expected schema

### Debug Commands

```bash
# Check database schema
sqlite3 backend/events.db ".schema events"

# Test API endpoint
curl -X GET "http://localhost:8000/api/events"

# Check backend logs
cd backend
uvicorn main:app --reload --log-level debug
``` 