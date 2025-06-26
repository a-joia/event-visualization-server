"""
EventHawk Client - Main client for interacting with the Dashboard API
"""

import requests
import json
from typing import Optional, List
from datetime import datetime

try:
    from .models import Event, EventCreate, EventUpdate, EventListResponse
except ImportError:
    from models import Event, EventCreate, EventUpdate, EventListResponse

class EventHawkClient:
    """Client for interacting with the Dashboard API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the EventHawk client
        
        Args:
            base_url: Base URL of the API server (default: http://localhost:8000)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make an HTTP request to the API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            **kwargs: Additional arguments for requests
            
        Returns:
            requests.Response object
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise Exception(f"API request failed: {e}")
    
    def health_check(self) -> dict:
        """
        Check API health
        
        Returns:
            Health status dictionary
        """
        response = self._make_request('GET', '/api/health')
        return response.json()
    
    def create_event(self, event: EventCreate) -> Event:
        """
        Create a new event
        
        Args:
            event: EventCreate object with event data
            
        Returns:
            Created Event object
        """
        response = self._make_request(
            'POST', 
            '/api/events', 
            json=event.to_dict()
        )
        return Event.from_dict(response.json())
    
    def get_event(self, event_id: int) -> Event:
        """
        Get a single event by ID
        
        Args:
            event_id: ID of the event to retrieve
            
        Returns:
            Event object
            
        Raises:
            Exception: If event is not found
        """
        response = self._make_request('GET', f'/api/events/{event_id}')
        return Event.from_dict(response.json())
    
    def get_events(
        self, 
        offset: int = 0, 
        limit: int = 20, 
        search_query: Optional[str] = None
    ) -> EventListResponse:
        """
        Get paginated list of events
        
        Args:
            offset: Number of events to skip (for pagination)
            limit: Maximum number of events to return
            search_query: Optional search query to filter events
            
        Returns:
            EventListResponse object with events and total count
        """
        params = {
            'offset': str(offset),
            'limit': str(limit)
        }
        if search_query:
            params['q'] = search_query
        
        response = self._make_request('GET', '/api/events', params=params)
        return EventListResponse.from_dict(response.json())
    
    def update_event(self, event_id: int, event_update: EventUpdate) -> Event:
        """
        Update an existing event
        
        Args:
            event_id: ID of the event to update
            event_update: EventUpdate object with fields to update
            
        Returns:
            Updated Event object
            
        Raises:
            Exception: If event is not found
        """
        response = self._make_request(
            'PUT', 
            f'/api/events/{event_id}', 
            json=event_update.to_dict()
        )
        return Event.from_dict(response.json())
    
    def delete_event(self, event_id: int) -> bool:
        """
        Delete an event
        
        Args:
            event_id: ID of the event to delete
            
        Returns:
            True if deletion was successful
            
        Raises:
            Exception: If event is not found
        """
        self._make_request('DELETE', f'/api/events/{event_id}')
        return True
    
    def search_events(self, query: str, limit: int = 20) -> List[Event]:
        """
        Search for events by query
        
        Args:
            query: Search query string
            limit: Maximum number of events to return
            
        Returns:
            List of matching Event objects
        """
        response = self.get_events(offset=0, limit=limit, search_query=query)
        return response.events
    
    def get_events_by_status(self, status: str, limit: int = 20) -> List[Event]:
        """
        Get events filtered by status
        
        Args:
            status: Status to filter by (e.g., 'pending', 'solved', 'threat')
            limit: Maximum number of events to return
            
        Returns:
            List of Event objects with matching status
        """
        # Get events in batches to respect the backend limit
        all_matching_events = []
        offset = 0
        batch_size = min(100, limit)  # Backend max is 100
        
        while len(all_matching_events) < limit:
            response = self.get_events(offset=offset, limit=batch_size)
            
            # Filter by status
            matching_events = [event for event in response.events if event.status == status]
            all_matching_events.extend(matching_events)
            
            # If no more events or we have enough, break
            if len(response.events) < batch_size or len(all_matching_events) >= limit:
                break
                
            offset += batch_size
        
        return all_matching_events[:limit]
    
    def get_events_by_tag(self, tag: str, limit: int = 20) -> List[Event]:
        """
        Get events filtered by tag
        
        Args:
            tag: Tag to filter by
            limit: Maximum number of events to return
            
        Returns:
            List of Event objects with matching tag
        """
        # Get events in batches to respect the backend limit
        all_matching_events = []
        offset = 0
        batch_size = min(100, limit)  # Backend max is 100
        
        while len(all_matching_events) < limit:
            response = self.get_events(offset=offset, limit=batch_size)
            
            # Filter by tag
            matching_events = [event for event in response.events if event.tag == tag]
            all_matching_events.extend(matching_events)
            
            # If no more events or we have enough, break
            if len(response.events) < batch_size or len(all_matching_events) >= limit:
                break
                
            offset += batch_size
        
        return all_matching_events[:limit]
    
    def get_recent_events(self, hours: int = 24, limit: int = 20) -> List[Event]:
        """
        Get recent events from the last N hours
        
        Args:
            hours: Number of hours to look back
            limit: Maximum number of events to return
            
        Returns:
            List of recent Event objects
        """
        # Get events in batches to respect the backend limit
        all_recent_events = []
        offset = 0
        batch_size = min(100, limit)  # Backend max is 100
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        
        while len(all_recent_events) < limit:
            response = self.get_events(offset=offset, limit=batch_size)
            
            # Filter by time
            for event in response.events:
                try:
                    event_time = datetime.fromisoformat(event.time.replace('Z', '+00:00')).timestamp()
                    if event_time >= cutoff_time:
                        all_recent_events.append(event)
                        if len(all_recent_events) >= limit:
                            break
                except:
                    # Skip events with invalid time format
                    continue
            
            # If no more events, break
            if len(response.events) < batch_size:
                break
                
            offset += batch_size
        
        return all_recent_events[:limit]
    
    def close(self):
        """Close the client session"""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close() 