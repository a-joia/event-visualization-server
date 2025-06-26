"""
Examples of how to use the EventHawk client library
"""

from datetime import datetime
try:
    from .client import EventHawkClient
    from .models import EventCreate, EventUpdate
except ImportError:
    from client import EventHawkClient
    from models import EventCreate, EventUpdate

def basic_usage_example():
    """Basic usage example"""
    print("=== Basic Usage Example ===")
    
    # Create client
    client = EventHawkClient("http://localhost:8000")
    
    # Check API health
    health = client.health_check()
    print(f"API Health: {health}")
    
    # Get all events
    events_response = client.get_events(offset=0, limit=10)
    print(f"Found {events_response.total} events")
    
    for event in events_response.events:
        print(f"- {event.name} (ID: {event.id}, Status: {event.status})")
    
    client.close()

def create_event_example():
    """Example of creating a new event"""
    print("\n=== Create Event Example ===")
    
    with EventHawkClient("http://localhost:8000") as client:
        # Create a new event
        new_event = EventCreate(
            id=999,
            name="Test Event from Client",
            summary="This is a test event created via the client library",
            status="pending",
            tag="test",
            time=datetime.now().isoformat(),
            description="## Test Event\n\nThis event was created using the EventHawk client library."
        )
        
        try:
            created_event = client.create_event(new_event)
            print(f"Created event: {created_event.name} (ID: {created_event.id})")
        except Exception as e:
            print(f"Error creating event: {e}")

def update_event_example():
    """Example of updating an event"""
    print("\n=== Update Event Example ===")
    
    with EventHawkClient("http://localhost:8000") as client:
        event_id = 123  # Replace with actual event ID
        
        # Update event
        update_data = EventUpdate(
            status="solved",
            description="## Updated Event\n\nThis event has been updated via the client library."
        )
        
        try:
            updated_event = client.update_event(event_id, update_data)
            print(f"Updated event: {updated_event.name} (Status: {updated_event.status})")
        except Exception as e:
            print(f"Error updating event: {e}")

def search_events_example():
    """Example of searching events"""
    print("\n=== Search Events Example ===")
    
    with EventHawkClient("http://localhost:8000") as client:
        # Search for events containing "API"
        search_results = client.search_events("API", limit=5)
        print(f"Found {len(search_results)} events containing 'API':")
        
        for event in search_results:
            print(f"- {event.name} (ID: {event.id})")

def filter_events_example():
    """Example of filtering events"""
    print("\n=== Filter Events Example ===")
    
    with EventHawkClient("http://localhost:8000") as client:
        # Get events by status
        pending_events = client.get_events_by_status("pending", limit=5)
        print(f"Found {len(pending_events)} pending events:")
        
        for event in pending_events:
            print(f"- {event.name} (ID: {event.id})")
        
        # Get events by tag
        system_events = client.get_events_by_tag("system", limit=5)
        print(f"\nFound {len(system_events)} system events:")
        
        for event in system_events:
            print(f"- {event.name} (ID: {event.id})")

def recent_events_example():
    """Example of getting recent events"""
    print("\n=== Recent Events Example ===")
    
    with EventHawkClient("http://localhost:8000") as client:
        # Get events from the last 24 hours
        recent_events = client.get_recent_events(hours=24, limit=5)
        print(f"Found {len(recent_events)} events from the last 24 hours:")
        
        for event in recent_events:
            print(f"- {event.name} (Time: {event.time})")

def delete_event_example():
    """Example of deleting an event"""
    print("\n=== Delete Event Example ===")
    
    with EventHawkClient("http://localhost:8000") as client:
        event_id = 999  # Replace with actual event ID
        
        try:
            success = client.delete_event(event_id)
            if success:
                print(f"Successfully deleted event {event_id}")
        except Exception as e:
            print(f"Error deleting event: {e}")

def pagination_example():
    """Example of pagination"""
    print("\n=== Pagination Example ===")
    
    with EventHawkClient("http://localhost:8000") as client:
        page_size = 5  # Use smaller page size
        page = 0
        
        while True:
            offset = page * page_size
            response = client.get_events(offset=offset, limit=page_size)
            
            print(f"Page {page + 1}:")
            for event in response.events:
                print(f"  - {event.name} (ID: {event.id})")
            
            if len(response.events) < page_size:
                break
            
            page += 1

def main():
    """Run all examples"""
    print("EventHawk Client Library Examples")
    print("=" * 50)
    
    try:
        basic_usage_example()
        create_event_example()
        update_event_example()
        search_events_example()
        filter_events_example()
        recent_events_example()
        delete_event_example()
        pagination_example()
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure the backend server is running on http://localhost:8000")

if __name__ == "__main__":
    main() 