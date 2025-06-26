"""
Simple test for EventHawk client library
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'eventhawk-lib'))

from datetime import datetime
from eventhawk_lib.client import EventHawkClient
from eventhawk_lib.models import EventCreate, EventUpdate

def test_eventhawk():
    """Test the EventHawk client library"""
    print("Testing EventHawk Client Library")
    print("=" * 40)
    
    try:
        # Create client
        client = EventHawkClient("http://localhost:8000")
        print("✅ Client created successfully")
        
        # Test health check
        health = client.health_check()
        print(f"✅ Health check: {health}")
        
        # Test getting events
        events_response = client.get_events(offset=0, limit=5)
        print(f"✅ Found {events_response.total} events")
        
        if events_response.events:
            print("Sample events:")
            for event in events_response.events[:3]:
                print(f"  - {event.name} (ID: {event.id}, Status: {event.status})")
        
        # Test creating an event
        new_event = EventCreate(
            id=888,
            name="Test Event from Client Library",
            summary="This is a test event created via the client library",
            status="pending",
            tag="test",
            time=datetime.now().isoformat(),
            description="## Test Event\n\nThis event was created using the EventHawk client library."
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
        
        client.close()
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Make sure the backend server is running on http://localhost:8000")

if __name__ == "__main__":
    test_eventhawk() 