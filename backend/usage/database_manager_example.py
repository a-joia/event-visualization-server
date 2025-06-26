"""
Example Usage of DatabaseManager
-------------------------------
This script demonstrates how to use the DatabaseManager class
with the three main functions: init_database(), get_from_database(), and write_to_database().
"""

import asyncio
import sys
import os

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_manager import db_manager

async def main():
    """Example usage of DatabaseManager"""
    
    print("=== DatabaseManager Example Usage ===\n")
    
    # 1. Initialize the database
    print("1. Initializing database...")
    success = await db_manager.init_database()
    if success:
        print("✅ Database initialized successfully!")
    else:
        print("❌ Failed to initialize database")
        return
    
    # 2. Write data to database (INSERT)
    print("\n2. Writing sample events to database...")
    
    sample_events = [
        {
            "id": 1,
            "name": "System Startup",
            "summary": "Application started successfully",
            "status": "completed",
            "tag": "system",
            "time": "2024-01-15T10:00:00Z",
            "description": "The application has been started and is running normally.",
            "event_start": "2024-01-15T10:00:00Z",
            "event_end": "2024-01-15T10:05:00Z"
        },
        {
            "id": 2,
            "name": "User Login",
            "summary": "User authentication successful",
            "status": "active",
            "tag": "auth",
            "time": "2024-01-15T10:05:00Z",
            "description": "User john.doe has successfully logged into the system.",
            "event_start": "2024-01-15T10:05:00Z",
            "event_end": "2024-01-15T11:30:00Z"
        },
        {
            "id": 3,
            "name": "Data Export",
            "summary": "Export operation completed",
            "status": "completed",
            "tag": "export",
            "time": "2024-01-15T10:10:00Z",
            "description": "Data export to CSV format has been completed successfully.",
            "event_start": "2024-01-15T10:10:00Z",
            "event_end": "2024-01-15T10:15:00Z"
        }
    ]
    
    # Insert all events
    success = await db_manager.write_to_database(
        table_name="events",
        data=sample_events,
        operation="insert"
    )
    
    if success:
        print("✅ Sample events inserted successfully!")
    else:
        print("❌ Failed to insert sample events")
        return
    
    # 3. Get data from database (SELECT)
    print("\n3. Reading events from database...")
    
    # Get all events
    all_events = await db_manager.get_from_database(
        table_name="events",
        limit=10,
        order_by="id"
    )
    
    print(f"📊 Found {len(all_events)} events:")
    for event in all_events:
        print(f"   - ID: {event['id']}, Name: {event['name']}, Status: {event['status']}")
    
    # Get events with filter
    print("\n4. Filtering events by status...")
    active_events = await db_manager.get_from_database(
        table_name="events",
        filters={"status": "active"}
    )
    
    print(f"📊 Found {len(active_events)} active events:")
    for event in active_events:
        print(f"   - ID: {event['id']}, Name: {event['name']}")
    
    # Search events
    print("\n5. Searching events...")
    search_results = await db_manager.get_from_database(
        table_name="events",
        search_query="export",
        limit=5
    )
    
    print(f"🔍 Found {len(search_results)} events matching 'export':")
    for event in search_results:
        print(f"   - ID: {event['id']}, Name: {event['name']}")
    
    # 6. Update data in database (UPDATE)
    print("\n6. Updating an event...")
    
    update_data = {
        "id": 2,
        "status": "completed",
        "description": "User john.doe has successfully logged into the system and completed their session."
    }
    
    success = await db_manager.write_to_database(
        table_name="events",
        data=update_data,
        operation="update"
    )
    
    if success:
        print("✅ Event updated successfully!")
        
        # Verify the update
        updated_event = await db_manager.get_from_database(
            table_name="events",
            filters={"id": 2}
        )
        
        if updated_event:
            print(f"   - Updated status: {updated_event[0]['status']}")
            print(f"   - Updated description: {updated_event[0]['description']}")
    else:
        print("❌ Failed to update event")
    
    # 7. Count records
    print("\n7. Counting records...")
    
    total_count = await db_manager.count_records(table_name="events")
    completed_count = await db_manager.count_records(
        table_name="events",
        filters={"status": "completed"}
    )
    
    print(f"📊 Total events: {total_count}")
    print(f"📊 Completed events: {completed_count}")
    
    # 8. Delete data from database (DELETE)
    print("\n8. Deleting an event...")
    
    delete_data = {"id": 3}
    
    success = await db_manager.write_to_database(
        table_name="events",
        data=delete_data,
        operation="delete"
    )
    
    if success:
        print("✅ Event deleted successfully!")
        
        # Verify the deletion
        remaining_count = await db_manager.count_records(table_name="events")
        print(f"📊 Remaining events: {remaining_count}")
    else:
        print("❌ Failed to delete event")
    
    print("\n=== Example completed successfully! ===")

if __name__ == "__main__":
    asyncio.run(main()) 