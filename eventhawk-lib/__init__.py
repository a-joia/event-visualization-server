"""
EventHawk Library - Client library for interacting with the Dashboard API
"""

from .client import EventHawkClient
from .models import Event, EventCreate, EventUpdate

__version__ = "1.0.0"
__all__ = ["EventHawkClient", "Event", "EventCreate", "EventUpdate"] 