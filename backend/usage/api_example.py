"""
API Usage Example
----------------
This script demonstrates how to interact with the FastAPI endpoints
programmatically using the requests library.
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000/api"

def test_api_endpoints():
    """Test all API endpoints"""
    
    print("=== API Usage Example ===\n")
    
    # 1. Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL.replace('/api', '')}/api/health")
        if response.status_code == 200:
            print("✅ API is running!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running on http://localhost:8000")
        return
    
    # 2. Create events
    print("\n2. Creating sample events...")
    
    sample_events = [
        {
            "id": 101,
            "name": "API Test Event 1",
            "summary": "Testing API creation",
            "status": "active",
            "tag": "test",
            "time": "2024-01-15T12:00:00Z",
            "description": "This is a test event created via API.",
            "event_start": "2024-01-15T12:00:00Z",
            "event_end": "2024-01-15T13:00:00Z"
        },
        {
            "id": 102,
            "name": "API Test Event 2",
            "summary": "Another test event",
            "status": "pending",
            "tag": "test",
            "time": "2024-01-15T12:05:00Z",
            "description": "Second test event for API testing.",
            "event_start": "2024-01-15T12:05:00Z",
            "event_end": "2024-01-15T12:30:00Z"
        }
    ]
    
    created_events = []
    for event in sample_events:
        response = requests.post(f"{BASE_URL}/events", json=event)
        if response.status_code == 201:
            created_event = response.json()
            created_events.append(created_event)
            print(f"✅ Created event: {created_event['name']} (ID: {created_event['id']})")
        else:
            print(f"❌ Failed to create event: {response.status_code} - {response.text}")
    
    # 3. Get all events
    print("\n3. Getting all events...")
    response = requests.get(f"{BASE_URL}/events?limit=10")
    if response.status_code == 200:
        events_data = response.json()
        print(f"✅ Retrieved {len(events_data['events'])} events (Total: {events_data['total']})")
        for event in events_data['events'][:3]:  # Show first 3
            print(f"   - ID: {event['id']}, Name: {event['name']}, Status: {event['status']}")
    else:
        print(f"❌ Failed to get events: {response.status_code}")
    
    # 4. Get specific event
    if created_events:
        print(f"\n4. Getting specific event (ID: {created_events[0]['id']})...")
        response = requests.get(f"{BASE_URL}/events/{created_events[0]['id']}")
        if response.status_code == 200:
            event = response.json()
            print(f"✅ Retrieved event: {event['name']}")
            print(f"   Status: {event['status']}")
            print(f"   Description: {event['description']}")
        else:
            print(f"❌ Failed to get event: {response.status_code}")
    
    # 5. Update event
    if created_events:
        print(f"\n5. Updating event (ID: {created_events[0]['id']})...")
        update_data = {
            "status": "completed",
            "description": "Updated via API call"
        }
        response = requests.put(f"{BASE_URL}/events/{created_events[0]['id']}", json=update_data)
        if response.status_code == 200:
            updated_event = response.json()
            print(f"✅ Updated event: {updated_event['name']}")
            print(f"   New status: {updated_event['status']}")
        else:
            print(f"❌ Failed to update event: {response.status_code}")
    
    # 6. Search events
    print("\n6. Searching events...")
    response = requests.get(f"{BASE_URL}/events?q=test&limit=5")
    if response.status_code == 200:
        search_data = response.json()
        print(f"✅ Found {len(search_data['events'])} events matching 'test'")
        for event in search_data['events']:
            print(f"   - ID: {event['id']}, Name: {event['name']}")
    else:
        print(f"❌ Failed to search events: {response.status_code}")
    
    # 7. Get events by status
    print("\n7. Getting events by status...")
    response = requests.get(f"{BASE_URL}/events/status/active")
    if response.status_code == 200:
        status_data = response.json()
        print(f"✅ Found {len(status_data['events'])} active events")
        for event in status_data['events']:
            print(f"   - ID: {event['id']}, Name: {event['name']}")
    else:
        print(f"❌ Failed to get events by status: {response.status_code}")
    
    # 8. Get event counts
    print("\n8. Getting event statistics...")
    response = requests.get(f"{BASE_URL}/events/stats/counts")
    if response.status_code == 200:
        stats = response.json()
        print("✅ Event statistics:")
        for status, count in stats.items():
            print(f"   - {status}: {count}")
    else:
        print(f"❌ Failed to get statistics: {response.status_code}")
    
    # 9. Delete events (cleanup)
    print("\n9. Cleaning up test events...")
    for event in created_events:
        response = requests.delete(f"{BASE_URL}/events/{event['id']}")
        if response.status_code == 204:
            print(f"✅ Deleted event: {event['name']}")
        else:
            print(f"❌ Failed to delete event {event['id']}: {response.status_code}")
    
    print("\n=== API Example completed successfully! ===")

if __name__ == "__main__":
    test_api_endpoints() 