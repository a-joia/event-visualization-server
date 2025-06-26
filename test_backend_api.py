#!/usr/bin/env python3
"""
Simple test script to verify the backend API is working correctly.
"""

import requests
import json

def test_backend_api():
    """Test the backend API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Backend API...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test events endpoint
    try:
        response = requests.get(f"{base_url}/api/events")
        print(f"✅ Events endpoint: {response.status_code}")
        data = response.json()
        print(f"   Total events: {data.get('total', 0)}")
        print(f"   Events returned: {len(data.get('events', []))}")
        
        if data.get('events'):
            print("   Sample event:")
            event = data['events'][0]
            print(f"     ID: {event.get('id')}")
            print(f"     Name: {event.get('name')}")
            print(f"     Status: {event.get('status')}")
            print(f"     Start: {event.get('event_start')}")
            print(f"     End: {event.get('event_end')}")
        
    except Exception as e:
        print(f"❌ Events endpoint failed: {e}")
        return False
    
    print("\n🎉 Backend API is working correctly!")
    return True

if __name__ == "__main__":
    test_backend_api() 