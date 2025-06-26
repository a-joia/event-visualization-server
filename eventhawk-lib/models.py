"""
Data models for EventHawk client library
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Event:
    """Event data model"""
    id: int
    name: str
    summary: str
    status: str
    tag: str
    time: str
    description: str
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        """Create Event from dictionary"""
        return cls(**data)
    
    def to_dict(self) -> dict:
        """Convert Event to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'summary': self.summary,
            'status': self.status,
            'tag': self.tag,
            'time': self.time,
            'description': self.description
        }

@dataclass
class EventCreate:
    """Event creation data model"""
    id: int
    name: str
    summary: str
    status: str
    tag: str
    time: str
    description: str
    
    def to_dict(self) -> dict:
        """Convert EventCreate to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'summary': self.summary,
            'status': self.status,
            'tag': self.tag,
            'time': self.time,
            'description': self.description
        }

@dataclass
class EventUpdate:
    """Event update data model"""
    name: Optional[str] = None
    summary: Optional[str] = None
    status: Optional[str] = None
    tag: Optional[str] = None
    time: Optional[str] = None
    description: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert EventUpdate to dictionary, excluding None values"""
        return {k: v for k, v in self.__dict__.items() if v is not None}

@dataclass
class EventListResponse:
    """Response model for paginated event list"""
    events: list[Event]
    total: int
    
    @classmethod
    def from_dict(cls, data: dict) -> 'EventListResponse':
        """Create EventListResponse from dictionary"""
        events = [Event.from_dict(event_data) for event_data in data.get('events', [])]
        return cls(events=events, total=data.get('total', 0)) 