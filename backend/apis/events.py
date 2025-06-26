from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from services import EventService
from schemas import EventCreate, EventResponse, EventListResponse, EventUpdate
from kusto import KustoHandler

router = APIRouter()

# Create service instance
event_service = EventService()
kusto_handler = KustoHandler()

@router.post("/events", response_model=EventResponse, status_code=201)
async def create_event(event: EventCreate):
    """Create a new event"""
    event_data = await event_service.create_event(event)
    return EventResponse.model_validate(event_data)

@router.get("/events", response_model=EventListResponse)
async def get_events(
    offset: int = Query(0, ge=0, description="Number of events to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of events to return"),
    q: Optional[str] = Query(None, description="Search query")
):
    """Get paginated list of events with optional search"""
    events, total = await event_service.get_events(offset, limit, q)
    
    return EventListResponse(
        events=[EventResponse.model_validate(event) for event in events],
        total=total
    )

@router.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int):
    """Get a single event by ID"""
    event_data = await event_service.get_event(event_id)
    return EventResponse.model_validate(event_data)

@router.put("/events/{event_id}", response_model=EventResponse)
async def update_event(event_id: int, event_data: EventUpdate):
    """Update an existing event"""
    updated_event = await event_service.update_event(event_id, event_data)
    return EventResponse.model_validate(updated_event)

@router.delete("/events/{event_id}", status_code=204)
async def delete_event(event_id: int):
    """Delete an event"""
    await event_service.delete_event(event_id)
    return None

@router.get("/events/status/{status}", response_model=EventListResponse)
async def get_events_by_status(status: str):
    """Get all events with a specific status"""
    events = await event_service.get_events_by_status(status)
    return EventListResponse(
        events=[EventResponse.model_validate(event) for event in events],
        total=len(events)
    )

@router.get("/events/tag/{tag}", response_model=EventListResponse)
async def get_events_by_tag(tag: str):
    """Get all events with a specific tag"""
    events = await event_service.get_events_by_tag(tag)
    return EventListResponse(
        events=[EventResponse.model_validate(event) for event in events],
        total=len(events)
    )

@router.get("/events/stats/counts")
async def get_event_counts():
    """Get count of events grouped by status"""
    return await event_service.get_event_count_by_status()

@router.get("/events/analytics/kusto-data")
async def get_kusto_data():
    """Get kusto test data for analytics charts"""
    try:
        data = kusto_handler.get_data("test_query")
        # Convert datetime objects to strings for JSON serialization
        if data and "timestamp" in data:
            # Check if timestamps are already strings or datetime objects
            if data["timestamp"] and hasattr(data["timestamp"][0], 'isoformat'):
                data["timestamp"] = [ts.isoformat() for ts in data["timestamp"]]
            # If they're already strings, leave them as is
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching kusto data: {str(e)}")

@router.get("/events/analytics/bar-features")
async def get_bar_features():
    """Get available categorical features for bar plot"""
    try:
        features = kusto_handler.get_available_features()
        return {"features": features}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bar features: {str(e)}")

@router.get("/events/analytics/bar-data")
async def get_bar_data(
    feature: str = Query(..., description="Feature to analyze"),
    start_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date (YYYY-MM-DD)"),
    bin_size: str = Query("1D", description="Bin size: 1H, 1D, 1W")
):
    """Get bar plot data for a specific feature with date range and bin size"""
    try:
        data = kusto_handler.get_bar_data(feature, start_date, end_date, bin_size)
        return {"data": data, "feature": feature, "bin_size": bin_size}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bar data: {str(e)}")

@router.post("/events/analytics/cache/clear")
async def clear_cache():
    """Clear all cached data"""
    try:
        kusto_handler.clear_cache()
        return {"message": "Cache cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")

@router.get("/events/analytics/cache/status")
async def get_cache_status():
    """Get cache status information"""
    try:
        status = kusto_handler.get_cache_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting cache status: {str(e)}") 