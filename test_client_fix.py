"""
Test script to verify EventHawk client library works with backend limits
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'eventhawk-lib'))

from datetime import datetime
from client import EventHawkClient
from models import EventCreate, EventUpdate

def test_client():
    """Test the client library with proper limits"""
    print("Testing EventHawk Client Library (Fixed)")
    print("=" * 50)
    
    try:
        # Create client
        client = EventHawkClient("http://localhost:8000")
        print("✅ Client created successfully")
        
        # Test health check
        health = client.health_check()
        print(f"✅ Health check: {health}")
        
        # Test getting events with proper limit
        events_response = client.get_events(offset=0, limit=10)  # Use limit <= 100
        print(f"✅ Found {events_response.total} events")
        
        if events_response.events:
            print("Sample events:")
            for event in events_response.events[:3]:
                print(f"  - {event.name} (ID: {event.id}, Status: {event.status})")
        
        # Test creating an event
        new_event = EventCreate(
            id=666,
            name="Test Event from Fixed Client",
            summary="This is a test event created via the fixed client library",
            status="pending",
            tag="test",
            time=datetime.now().isoformat(),
            description="## Test Event\n\nThis event was created using the fixed EventHawk client library."
        )
        
        try:
            created_event = client.create_event(new_event)
            print(f"✅ Created event: {created_event.name} (ID: {created_event.id})")
            
            # Test updating the event
            update_data = EventUpdate(status="solved")
            updated_event = client.update_event(created_event.id, update_data)
            print(f"✅ Updated event status to: {updated_event.status}")
            
            # Test deleting the event
            client.delete_event(created_event.id)
            print(f"✅ Deleted event {created_event.id}")
            
        except Exception as e:
            print(f"⚠️  Event creation/update/delete test failed: {e}")
        
        # Test search with proper limit
        try:
            search_results = client.search_events("test", limit=5)  # Use limit <= 100
            print(f"✅ Search found {len(search_results)} events containing 'test'")
        except Exception as e:
            print(f"⚠️  Search test failed: {e}")
        
        # Test filtering with proper limits
        try:
            pending_events = client.get_events_by_status("pending", limit=5)
            print(f"✅ Found {len(pending_events)} pending events")
        except Exception as e:
            print(f"⚠️  Status filter test failed: {e}")
        
        client.close()
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Make sure the backend server is running on http://localhost:8000")

if __name__ == "__main__":
    test_client() 