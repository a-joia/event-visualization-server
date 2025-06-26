from sqlalchemy import Column, Integer, String, Text
from database import Base

class Event(Base):
    """Database model for events"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    status = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    time = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    event_start = Column(String, nullable=True)  # Event start datetime
    event_end = Column(String, nullable=True)    # Event end datetime
    
    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', status='{self.status}')>" 