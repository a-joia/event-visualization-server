"""
Event Times Example
------------------
This script demonstrates how to work with the new event_start and event_end fields,
including filtering events by time ranges and duration calculations.
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_manager import db_manager

def format_datetime(dt):
    """Format datetime to ISO string"""
    return dt.isoformat() + "Z"

async def main():
    """Example usage of event time fields"""
    
    print("=== Event Times Example ===\n")
    
    # 1. Initialize the database
    print("1. Initializing database...")
    success = await db_manager.init_database()
    if success:
        print("✅ Database initialized successfully!")
    else:
        print("❌ Failed to initialize database")
        return
    
    # 2. Create events with different time ranges
    print("\n2. Creating events with time ranges...")
    
    # Create events spanning different time periods
    base_time = datetime(2024, 1, 15, 10, 0, 0)
    
    time_events = [
        {
            "id": 301,
            "name": "Morning Meeting",
            "summary": "Daily standup meeting",
            "status": "completed",
            "tag": "meeting",
            "time": format_datetime(base_time),
            "description": "Daily team standup meeting",
            "event_start": format_datetime(base_time),
            "event_end": format_datetime(base_time + timedelta(hours=1))
        },
        {
            "id": 302,
            "name": "Lunch Break",
            "summary": "Team lunch",
            "status": "completed",
            "tag": "break",
            "time": format_datetime(base_time + timedelta(hours=2)),
            "description": "Team lunch break",
            "event_start": format_datetime(base_time + timedelta(hours=2)),
            "event_end": format_datetime(base_time + timedelta(hours=3))
        },
        {
            "id": 303,
            "name": "Afternoon Workshop",
            "summary": "Technical workshop",
            "status": "active",
            "tag": "workshop",
            "time": format_datetime(base_time + timedelta(hours=4)),
            "description": "Technical workshop on new features",
            "event_start": format_datetime(base_time + timedelta(hours=4)),
            "event_end": format_datetime(base_time + timedelta(hours=6))
        },
        {
            "id": 304,
            "name": "Evening Review",
            "summary": "Code review session",
            "status": "pending",
            "tag": "review",
            "time": format_datetime(base_time + timedelta(hours=7)),
            "description": "Evening code review session",
            "event_start": format_datetime(base_time + timedelta(hours=7)),
            "event_end": format_datetime(base_time + timedelta(hours=8))
        }
    ]
    
    # Insert events
    success = await db_manager.write_to_database(
        table_name="events",
        data=time_events,
        operation="insert"
    )
    
    if success:
        print("✅ Time-based events created successfully!")
    else:
        print("❌ Failed to create time-based events")
        return
    
    # 3. Get all events with time information
    print("\n3. Getting all events with time information...")
    events = await db_manager.get_from_database(
        table_name="events",
        order_by="id"
    )
    
    print(f"📊 Found {len(events)} events:")
    for event in events:
        if event.get('event_start') and event.get('event_end'):
            start_time = event['event_start']
            end_time = event['event_end']
            print(f"   - {event['name']}: {start_time} to {end_time}")
        else:
            print(f"   - {event['name']}: No time range specified")
    
    # 4. Find events happening at a specific time
    print("\n4. Finding events happening at 11:00 AM...")
    target_time = format_datetime(base_time + timedelta(hours=1))  # 11:00 AM
    
    all_events = await db_manager.get_from_database(
        table_name="events",
        order_by="id"
    )
    
    happening_events = []
    for event in all_events:
        if event.get('event_start') and event.get('event_end'):
            start = event['event_start']
            end = event['event_end']
            if start <= target_time <= end:
                happening_events.append(event)
    
    print(f"📅 Events happening at {target_time}:")
    for event in happening_events:
        print(f"   - {event['name']} ({event['status']})")
    
    # 5. Find long-duration events (more than 1 hour)
    print("\n5. Finding long-duration events (> 1 hour)...")
    
    long_events = []
    for event in all_events:
        if event.get('event_start') and event.get('event_end'):
            start_dt = datetime.fromisoformat(event['event_start'].replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(event['event_end'].replace('Z', '+00:00'))
            duration = end_dt - start_dt
            
            if duration > timedelta(hours=1):
                long_events.append((event, duration))
    
    print("⏱️  Long-duration events:")
    for event, duration in long_events:
        hours = duration.total_seconds() / 3600
        print(f"   - {event['name']}: {hours:.1f} hours")
    
    # 6. Find upcoming events (events that haven't started yet)
    print("\n6. Finding upcoming events...")
    
    current_time = format_datetime(datetime.now())
    upcoming_events = []
    
    for event in all_events:
        if event.get('event_start') and event.get('event_end'):
            if event['event_start'] > current_time:
                upcoming_events.append(event)
    
    print(f"🔮 Upcoming events (after {current_time}):")
    for event in upcoming_events:
        print(f"   - {event['name']} starts at {event['event_start']}")
    
    # 7. Update event times
    print("\n7. Updating event times...")
    
    update_data = {
        "id": 301,
        "event_start": format_datetime(base_time + timedelta(minutes=30)),
        "event_end": format_datetime(base_time + timedelta(hours=1, minutes=30))
    }
    
    success = await db_manager.write_to_database(
        table_name="events",
        data=update_data,
        operation="update"
    )
    
    if success:
        print("✅ Event times updated successfully!")
        
        # Verify the update
        updated_event = await db_manager.get_from_database(
            table_name="events",
            filters={"id": 301}
        )
        
        if updated_event:
            event = updated_event[0]
            print(f"   - Updated: {event['name']}")
            print(f"   - New start: {event['event_start']}")
            print(f"   - New end: {event['event_end']}")
    else:
        print("❌ Failed to update event times")
    
    # 8. Calculate total event duration for the day
    print("\n8. Calculating total event duration for the day...")
    
    total_duration = timedelta()
    events_with_times = [e for e in all_events if e.get('event_start') and e.get('event_end')]
    
    for event in events_with_times:
        start_dt = datetime.fromisoformat(event['event_start'].replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(event['event_end'].replace('Z', '+00:00'))
        duration = end_dt - start_dt
        total_duration += duration
    
    total_hours = total_duration.total_seconds() / 3600
    print(f"📊 Total event duration: {total_hours:.1f} hours")
    
    # 9. Cleanup
    print("\n9. Cleaning up test events...")
    for event in time_events:
        success = await db_manager.write_to_database(
            table_name="events",
            data={"id": event['id']},
            operation="delete"
        )
        if success:
            print(f"✅ Deleted event: {event['name']}")
    
    print("\n=== Event Times Example completed successfully! ===")

if __name__ == "__main__":
    asyncio.run(main()) 