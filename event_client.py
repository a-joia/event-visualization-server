import requests
import datetime
import time

def create_event(api_url, event):
    """
    Create a new event via the API.
    event: dict with keys id, name, summary, status, tag, time, description
    """
    url = f"{api_url.rstrip('/')}/api/events"
    try:
        response = requests.post(url, json=event)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise

# Example usage:
if __name__ == "__main__":
    # Use timestamp as unique ID to avoid conflicts
    unique_id = int(time.time())
    event = {
        "id": unique_id,
        "name": f"API Created Event {unique_id}",
        "summary": "Created from Python client.",
        "status": "pending",
        "tag": "system",
        "time": datetime.datetime.now().isoformat(),
        "description": "## Created from Python This event was created using the Python client."
    }
    print(f"Creating event with ID: {unique_id}")
    result = create_event("http://localhost:8000", event)
    print(f"Success! Created event: {result}")
