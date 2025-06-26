#!/usr/bin/env python3
"""
Test script to add 20 new events with realistic data including event_start and event_end times.
"""

import asyncio
import random
from datetime import datetime, timedelta
from database_manager import DatabaseManager
from models import Event
from schemas import EventCreate

# Sample data for generating realistic events
EVENT_TYPES = [
    "System Maintenance",
    "Data Backup",
    "Security Scan",
    "Performance Monitoring",
    "User Training",
    "Software Update",
    "Network Maintenance",
    "Database Optimization",
    "Backup Verification",
    "System Health Check"
]

TAGS = [
    "critical",
    "high",
    "medium",
    "low",
    "urgent",
    "routine",
    "scheduled",
    "emergency"
]

STATUSES = ["active", "pending", "completed", "cancelled"]

DESCRIPTIONS = [
    "Scheduled maintenance window for system updates and optimization.",
    "Automated backup process to ensure data integrity and recovery.",
    "Security vulnerability scan to identify potential threats.",
    "Performance monitoring and analysis of system metrics.",
    "User training session for new features and best practices.",
    "Software update deployment with minimal downtime.",
    "Network infrastructure maintenance and optimization.",
    "Database performance tuning and index optimization.",
    "Backup integrity verification and restoration testing.",
    "Comprehensive system health check and diagnostics."
]

SUMMARIES = [
    "System maintenance completed successfully",
    "Backup process finished with no errors",
    "Security scan identified and resolved vulnerabilities",
    "Performance metrics within acceptable ranges",
    "Training session completed with positive feedback",
    "Software update deployed successfully",
    "Network maintenance completed without issues",
    "Database optimization improved query performance",
    "Backup verification confirmed data integrity",
    "System health check passed all diagnostics"
]

async def generate_test_events():
    """Generate 20 test events with realistic data."""
    db_manager = DatabaseManager()
    
    # Initialize database
    await db_manager.init_database()
    
    events_created = []
    
    for i in range(20):
        # Generate random event data
        event_type = random.choice(EVENT_TYPES)
        tag = random.choice(TAGS)
        status = random.choice(STATUSES)
        description = random.choice(DESCRIPTIONS)
        summary = random.choice(SUMMARIES)
        
        # Generate realistic timestamps
        # Base time: current time
        base_time = datetime.now()
        
        # Event start: between now and 30 days from now
        days_offset = random.randint(0, 30)
        hours_offset = random.randint(0, 23)
        minutes_offset = random.randint(0, 59)
        
        event_start = base_time + timedelta(
            days=days_offset,
            hours=hours_offset,
            minutes=minutes_offset
        )
        
        # Event end: between 1 hour and 8 hours after start
        duration_hours = random.randint(1, 8)
        duration_minutes = random.randint(0, 59)
        
        event_end = event_start + timedelta(
            hours=duration_hours,
            minutes=duration_minutes
        )
        
        # Create event data
        event_data = EventCreate(
            id=i+1,  # Use sequential ID
            name=f"{event_type} #{i+1}",  # Add required name field
            summary=f"{event_type} #{i+1}: {summary}",
            description=f"## {event_type}\n\n{description}\n\n**Event ID**: {i+1}\n**Priority**: {tag.upper()}\n**Duration**: {duration_hours}h {duration_minutes}m",
            status=status,
            tag=tag,
            time=base_time.isoformat(),
            event_start=event_start.isoformat(),
            event_end=event_end.isoformat()
        )
        
        try:
            # Add event to database using dict() method
            success = await db_manager.write_to_database("events", event_data.dict(), "insert")
            
            if success:
                # Get the created event to get its ID
                created_events = await db_manager.get_from_database(
                    table_name="events",
                    filters={"summary": event_data.summary},
                    limit=1
                )
                
                if created_events:
                    event_id = created_events[0].get("id", "unknown")
                    events_created.append({
                        "id": event_id,
                        "summary": event_data.summary,
                        "start": event_start.strftime("%Y-%m-%d %H:%M"),
                        "end": event_end.strftime("%Y-%m-%d %H:%M"),
                        "duration": f"{duration_hours}h {duration_minutes}m",
                        "status": status
                    })
                    
                    print(f"✅ Created event {i+1}/20: {event_data.summary}")
                    print(f"   ID: {event_id}")
                    print(f"   Start: {event_start.strftime('%Y-%m-%d %H:%M')}")
                    print(f"   End: {event_end.strftime('%Y-%m-%d %H:%M')}")
                    print(f"   Duration: {duration_hours}h {duration_minutes}m")
                    print(f"   Status: {status} | Tag: {tag}")
                    print()
                else:
                    print(f"⚠️  Event {i+1} created but couldn't retrieve ID")
            else:
                print(f"❌ Failed to create event {i+1}")
            
        except Exception as e:
            print(f"❌ Failed to create event {i+1}: {e}")
    
    print(f"\n🎉 Successfully created {len(events_created)} events!")
    print("\n📊 Summary:")
    print(f"   Total events created: {len(events_created)}")
    
    # Count by status
    status_counts = {}
    for event in events_created:
        status = event.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("   Events by status:")
    for status, count in status_counts.items():
        print(f"     {status}: {count}")
    
    return events_created

async def main():
    """Main function to run the test."""
    print("🚀 Starting test: Adding 20 new events...")
    print("=" * 60)
    
    try:
        events = await generate_test_events()
        print("\n✅ Test completed successfully!")
        print(f"📝 Created {len(events)} events with event_start and event_end times")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code) 