from typing import List, Optional, Sequence
from fastapi import HTTPException

from database_manager import db_manager
from schemas import EventCreate, EventUpdate

class EventService:
    """Service class for event-related operations using DatabaseManager"""
    
    def __init__(self):
        """Initialize the event service."""
        self.db_manager = db_manager
    
    async def create_event(self, event_data: EventCreate) -> dict:
        """Create a new event"""
        # Check if event with this ID already exists
        existing_events = await self.db_manager.get_from_database(
            table_name="events",
            filters={"id": event_data.id}
        )
        
        if existing_events:
            raise HTTPException(
                status_code=400, 
                detail=f'Event with ID {event_data.id} already exists'
            )
        
        # Create new event
        event_dict = event_data.dict()
        success = await self.db_manager.write_to_database(
            table_name="events",
            data=event_dict,
            operation="insert"
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create event")
        
        return event_dict
    
    async def get_event(self, event_id: int) -> dict:
        """Get a single event by ID"""
        events = await self.db_manager.get_from_database(
            table_name="events",
            filters={"id": event_id}
        )
        
        if not events:
            raise HTTPException(
                status_code=404, 
                detail=f'Event with ID {event_id} not found'
            )
        
        return events[0]
    
    async def get_events(
        self, 
        offset: int = 0, 
        limit: int = 20, 
        search_query: Optional[str] = None
    ) -> tuple[List[dict], int]:
        """Get paginated list of events with optional search"""
        # Get events with pagination and search
        events = await self.db_manager.get_from_database(
            table_name="events",
            limit=limit,
            offset=offset,
            search_query=search_query,
            order_by="id"
        )
        
        # Get total count
        total = await self.db_manager.count_records(
            table_name="events",
            filters={"id": None} if search_query else None  # Count all if no search
        )
        
        return events, total
    
    async def update_event(self, event_id: int, event_data: EventUpdate) -> dict:
        """Update an existing event"""
        # Check if event exists
        existing_events = await self.db_manager.get_from_database(
            table_name="events",
            filters={"id": event_id}
        )
        
        if not existing_events:
            raise HTTPException(
                status_code=404, 
                detail=f'Event with ID {event_id} not found'
            )
        
        # Prepare update data
        update_data = event_data.dict(exclude_unset=True)
        update_data['id'] = event_id  # Include ID for update operation
        
        # Update event
        success = await self.db_manager.write_to_database(
            table_name="events",
            data=update_data,
            operation="update"
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update event")
        
        # Return updated event
        return await self.get_event(event_id)
    
    async def delete_event(self, event_id: int) -> None:
        """Delete an event"""
        # Check if event exists
        existing_events = await self.db_manager.get_from_database(
            table_name="events",
            filters={"id": event_id}
        )
        
        if not existing_events:
            raise HTTPException(
                status_code=404, 
                detail=f'Event with ID {event_id} not found'
            )
        
        # Delete event
        success = await self.db_manager.write_to_database(
            table_name="events",
            data={"id": event_id},
            operation="delete"
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete event")
    
    async def get_events_by_status(self, status: str) -> List[dict]:
        """Get all events with a specific status"""
        return await self.db_manager.get_from_database(
            table_name="events",
            filters={"status": status}
        )
    
    async def get_events_by_tag(self, tag: str) -> List[dict]:
        """Get all events with a specific tag"""
        return await self.db_manager.get_from_database(
            table_name="events",
            filters={"tag": tag}
        )
    
    async def get_event_count_by_status(self) -> dict:
        """Get count of events grouped by status"""
        statuses = ["active", "pending", "completed", "failed", "cancelled"]
        counts = {}
        
        for status in statuses:
            count = await self.db_manager.count_records(
                table_name="events",
                filters={"status": status}
            )
            counts[status] = count
        
        return counts 