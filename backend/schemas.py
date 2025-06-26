from pydantic import BaseModel
from typing import List, Optional

class EventBase(BaseModel):
    """Base schema for event data"""
    name: str
    summary: str
    status: str
    tag: str
    time: str
    description: str
    event_start: Optional[str] = None
    event_end: Optional[str] = None

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
    event_start: Optional[str] = None
    event_end: Optional[str] = None

class EventResponse(EventBase):
    """Schema for event response"""
    id: int
    
    class Config:
        from_attributes = True

class EventListResponse(BaseModel):
    """Schema for paginated event list response"""
    events: List[EventResponse]
    total: int 