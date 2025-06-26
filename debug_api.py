import requests
import json
from datetime import datetime

def debug_api():
    try:
        print("Fetching API response from http://localhost:8000/api/events...")
        
        # Make the request
        response = requests.get('http://localhost:8000/api/events', timeout=10)
        
        # Create debug info
        debug_info = {
            "timestamp": datetime.now().isoformat(),
            "url": "http://localhost:8000/api/events",
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content_type": response.headers.get('content-type', 'unknown'),
            "content_length": len(response.content),
            "raw_content": response.text,
            "encoding": response.encoding
        }
        
        # Try to parse as JSON
        try:
            debug_info["json_parsed"] = response.json()
            debug_info["json_parse_success"] = True
        except json.JSONDecodeError as e:
            debug_info["json_parse_error"] = str(e)
            debug_info["json_parse_success"] = False
        
        # Save to file
        filename = f"api_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(debug_info, f, indent=2, ensure_ascii=False)
        
        print(f"Debug info saved to: {filename}")
        print(f"Status Code: {response.status_code}")
        print(f"Content Type: {response.headers.get('content-type', 'unknown')}")
        print(f"Content Length: {len(response.content)} bytes")
        print(f"First 200 characters: {response.text[:200]}")
        
        if response.status_code == 200:
            print("✅ API returned 200 OK")
        else:
            print(f"❌ API returned error status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server might not be running on port 8000")
        print("Make sure to run: cd backend && python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_api() 