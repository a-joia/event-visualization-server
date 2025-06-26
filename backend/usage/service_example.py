"""
Service Usage Example
--------------------
This script demonstrates how to use the EventService class directly
for business logic operations without going through the API layer.
"""

import asyncio
import sys
import os

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import EventService
from schemas import EventCreate, EventUpdate

async def main():
    """Example usage of EventService"""
    
    print("=== EventService Usage Example ===\n")
    
    # Create service instance
    service = EventService()
    
    # 1. Create events
    print("1. Creating sample events...")
    
    sample_events = [
        EventCreate(
            id=201,
            name="Service Test Event 1",
            summary="Testing service creation",
            status="active",
            tag="service",
            time="2024-01-15T13:00:00Z",
            description="This is a test event created via EventService.",
            event_start="2024-01-15T13:00:00Z",
            event_end="2024-01-15T14:00:00Z"
        ),
        EventCreate(
            id=202,
            name="Service Test Event 2",
            summary="Another service test",
            status="pending",
            tag="service",
            time="2024-01-15T13:05:00Z",
            description="Second test event for service testing.",
            event_start="2024-01-15T13:05:00Z",
            event_end="2024-01-15T13:30:00Z"
        ),
        EventCreate(
            id=203,
            name="Service Test Event 3",
            summary="Third test event",
            status="completed",
            tag="service",
            time="2024-01-15T13:10:00Z",
            description="Third test event with completed status.",
            event_start="2024-01-15T13:10:00Z",
            event_end="2024-01-15T13:20:00Z"
        )
    ]
    
    created_events = []
    for event_data in sample_events:
        try:
            event = await service.create_event(event_data)
            created_events.append(event)
            print(f"✅ Created event: {event['name']} (ID: {event['id']})")
        except Exception as e:
            print(f"❌ Failed to create event: {e}")
    
    # 2. Get all events with pagination
    print("\n2. Getting events with pagination...")
    try:
        events, total = await service.get_events(offset=0, limit=5)
        print(f"✅ Retrieved {len(events)} events (Total: {total})")
        for event in events:
            print(f"   - ID: {event['id']}, Name: {event['name']}, Status: {event['status']}")
    except Exception as e:
        print(f"❌ Failed to get events: {e}")
    
    # 3. Get specific event
    if created_events:
        print(f"\n3. Getting specific event (ID: {created_events[0]['id']})...")
        try:
            event = await service.get_event(created_events[0]['id'])
            print(f"✅ Retrieved event: {event['name']}")
            print(f"   Status: {event['status']}")
            print(f"   Description: {event['description']}")
        except Exception as e:
            print(f"❌ Failed to get event: {e}")
    
    # 4. Update event
    if created_events:
        print(f"\n4. Updating event (ID: {created_events[0]['id']})...")
        try:
            update_data = EventUpdate(
                status="completed",
                description="Updated via EventService"
            )
            updated_event = await service.update_event(created_events[0]['id'], update_data)
            print(f"✅ Updated event: {updated_event['name']}")
            print(f"   New status: {updated_event['status']}")
        except Exception as e:
            print(f"❌ Failed to update event: {e}")
    
    # 5. Search events
    print("\n5. Searching events...")
    try:
        events, total = await service.get_events(search_query="service", limit=10)
        print(f"✅ Found {len(events)} events matching 'service'")
        for event in events:
            print(f"   - ID: {event['id']}, Name: {event['name']}")
    except Exception as e:
        print(f"❌ Failed to search events: {e}")
    
    # 6. Get events by status
    print("\n6. Getting events by status...")
    try:
        active_events = await service.get_events_by_status("active")
        print(f"✅ Found {len(active_events)} active events")
        for event in active_events:
            print(f"   - ID: {event['id']}, Name: {event['name']}")
    except Exception as e:
        print(f"❌ Failed to get events by status: {e}")
    
    # 7. Get events by tag
    print("\n7. Getting events by tag...")
    try:
        service_events = await service.get_events_by_tag("service")
        print(f"✅ Found {len(service_events)} events with 'service' tag")
        for event in service_events:
            print(f"   - ID: {event['id']}, Name: {event['name']}")
    except Exception as e:
        print(f"❌ Failed to get events by tag: {e}")
    
    # 8. Get event statistics
    print("\n8. Getting event statistics...")
    try:
        stats = await service.get_event_count_by_status()
        print("✅ Event statistics:")
        for status, count in stats.items():
            print(f"   - {status}: {count}")
    except Exception as e:
        print(f"❌ Failed to get statistics: {e}")
    
    # 9. Delete events (cleanup)
    print("\n9. Cleaning up test events...")
    for event in created_events:
        try:
            await service.delete_event(event['id'])
            print(f"✅ Deleted event: {event['name']}")
        except Exception as e:
            print(f"❌ Failed to delete event {event['id']}: {e}")
    
    print("\n=== Service Example completed successfully! ===")

if __name__ == "__main__":
    asyncio.run(main()) 