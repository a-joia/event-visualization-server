"""
Database Manager Class
---------------------
This class provides a clean interface for all database operations.
It abstracts the underlying database implementation and makes it easy
to switch between different database backends (SQLite, PostgreSQL, Kusto, etc.).
"""

import asyncio
from typing import List, Dict, Any, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.exc import SQLAlchemyError
import logging

from db_provider import AsyncSessionLocal, Base, engine
from models import Event
from schemas import EventCreate, EventUpdate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Database manager class that provides a clean interface for all database operations.
    This class abstracts the underlying database implementation and can be easily
    extended to support different database backends.
    """
    
    def __init__(self):
        """Initialize the database manager."""
        self.session_factory = AsyncSessionLocal
        self.engine = engine
    
    async def init_database(self) -> bool:
        """
        Initialize the database and create all tables.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Initializing database...")
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database initialized successfully!")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            return False
    
    async def _get_session(self) -> AsyncSession:
        """
        Get a database session.
        
        Returns:
            AsyncSession: Database session
        """
        return self.session_factory()
    
    async def get_from_database(
        self, 
        table_name: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get data from the database with optional filtering, pagination, and search.
        
        Args:
            table_name (str): Name of the table to query
            filters (Dict[str, Any], optional): Dictionary of field-value pairs to filter by
            limit (int, optional): Maximum number of records to return
            offset (int, optional): Number of records to skip
            order_by (str, optional): Field to order by
            search_query (str, optional): Search query for text fields
            
        Returns:
            List[Dict[str, Any]]: List of records as dictionaries
        """
        try:
            async with await self._get_session() as session:
                # Get the model class based on table name
                model_class = self._get_model_class(table_name)
                if not model_class:
                    logger.error(f"Unknown table: {table_name}")
                    return []
                
                # Build the query
                stmt = select(model_class)
                
                # Apply filters
                if filters:
                    for field, value in filters.items():
                        if hasattr(model_class, field):
                            stmt = stmt.where(getattr(model_class, field) == value)
                
                # Apply search query (for text fields)
                if search_query:
                    search_conditions = []
                    for column in model_class.__table__.columns:
                        if hasattr(column.type, 'python_type') and column.type.python_type == str:
                            search_conditions.append(column.contains(search_query))
                    
                    if search_conditions:
                        from sqlalchemy import or_
                        stmt = stmt.where(or_(*search_conditions))
                
                # Apply ordering
                if order_by and hasattr(model_class, order_by):
                    stmt = stmt.order_by(getattr(model_class, order_by))
                
                # Apply pagination
                if offset:
                    stmt = stmt.offset(offset)
                if limit:
                    stmt = stmt.limit(limit)
                
                # Execute query
                result = await session.execute(stmt)
                records = result.scalars().all()
                
                # Convert to dictionaries
                return [self._model_to_dict(record) for record in records]
                
        except SQLAlchemyError as e:
            logger.error(f"Database query error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in get_from_database: {e}")
            return []
    
    async def write_to_database(
        self, 
        table_name: str, 
        data: Union[Dict[str, Any], List[Dict[str, Any]]], 
        operation: str = "insert"
    ) -> bool:
        """
        Write data to the database.
        
        Args:
            table_name (str): Name of the table to write to
            data (Union[Dict[str, Any], List[Dict[str, Any]]]): Data to write (single record or list of records)
            operation (str): Operation type - "insert", "update", or "delete"
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            async with await self._get_session() as session:
                # Get the model class based on table name
                model_class = self._get_model_class(table_name)
                if not model_class:
                    logger.error(f"Unknown table: {table_name}")
                    return False
                
                # Convert single record to list for uniform processing
                if isinstance(data, dict):
                    data = [data]
                
                if operation == "insert":
                    # Insert new records
                    for record_data in data:
                        # Remove None values
                        clean_data = {k: v for k, v in record_data.items() if v is not None}
                        db_record = model_class(**clean_data)
                        session.add(db_record)
                    
                    await session.commit()
                    logger.info(f"Successfully inserted {len(data)} record(s) into {table_name}")
                    
                elif operation == "update":
                    # Update existing records
                    for record_data in data:
                        if 'id' not in record_data:
                            logger.error("Update operation requires 'id' field")
                            return False
                        
                        # Get existing record
                        existing_record = await session.get(model_class, record_data['id'])
                        if not existing_record:
                            logger.error(f"Record with id {record_data['id']} not found")
                            return False
                        
                        # Update fields
                        for field, value in record_data.items():
                            if field != 'id' and hasattr(existing_record, field):
                                setattr(existing_record, field, value)
                    
                    await session.commit()
                    logger.info(f"Successfully updated {len(data)} record(s) in {table_name}")
                    
                elif operation == "delete":
                    # Delete records
                    for record_data in data:
                        if 'id' not in record_data:
                            logger.error("Delete operation requires 'id' field")
                            return False
                        
                        # Get existing record
                        existing_record = await session.get(model_class, record_data['id'])
                        if existing_record:
                            await session.delete(existing_record)
                    
                    await session.commit()
                    logger.info(f"Successfully deleted {len(data)} record(s) from {table_name}")
                    
                else:
                    logger.error(f"Unknown operation: {operation}")
                    return False
                
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Database write error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error in write_to_database: {e}")
            return False
    
    async def count_records(self, table_name: str, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count records in a table with optional filters.
        
        Args:
            table_name (str): Name of the table to count
            filters (Dict[str, Any], optional): Dictionary of field-value pairs to filter by
            
        Returns:
            int: Number of records
        """
        try:
            async with await self._get_session() as session:
                model_class = self._get_model_class(table_name)
                if not model_class:
                    return 0
                
                stmt = select(func.count()).select_from(model_class)
                
                # Apply filters
                if filters:
                    for field, value in filters.items():
                        if hasattr(model_class, field):
                            stmt = stmt.where(getattr(model_class, field) == value)
                
                result = await session.execute(stmt)
                return result.scalar_one()
                
        except SQLAlchemyError as e:
            logger.error(f"Database count error: {e}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error in count_records: {e}")
            return 0
    
    def _get_model_class(self, table_name: str):
        """
        Get the SQLAlchemy model class based on table name.
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            SQLAlchemy model class or None if not found
        """
        # Map table names to model classes
        model_mapping = {
            'events': Event,
            # Add more tables here as needed
        }
        
        return model_mapping.get(table_name.lower())
    
    def _model_to_dict(self, model_instance) -> Dict[str, Any]:
        """
        Convert a SQLAlchemy model instance to a dictionary.
        
        Args:
            model_instance: SQLAlchemy model instance
            
        Returns:
            Dict[str, Any]: Dictionary representation of the model
        """
        return {
            column.name: getattr(model_instance, column.name)
            for column in model_instance.__table__.columns
        }
    
    async def close(self):
        """Close database connections."""
        try:
            await self.engine.dispose()
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")


# Create a global instance
db_manager = DatabaseManager()


# Convenience functions for backward compatibility
async def get_from_database(*args, **kwargs):
    """Convenience function to get data from database."""
    return await db_manager.get_from_database(*args, **kwargs)


async def write_to_database(*args, **kwargs):
    """Convenience function to write data to database."""
    return await db_manager.write_to_database(*args, **kwargs)


async def init_database():
    """Convenience function to initialize database."""
    return await db_manager.init_database()


async def count_records(*args, **kwargs):
    """Convenience function to count records."""
    return await db_manager.count_records(*args, **kwargs) 