"""
Database Migration Script
-------------------------
Adds event_start and event_end columns to the events table.
Run this script to update existing databases with the new columns.
"""

import asyncio
import sqlite3
import os
from pathlib import Path

async def migrate_database():
    """Add event_start and event_end columns to events table"""
    
    # Get database path
    db_path = Path(__file__).parent / "events.db"
    
    if not db_path.exists():
        print("❌ Database file not found. Please run the application first to create the database.")
        return False
    
    print(f"📁 Database path: {db_path}")
    print("🔄 Starting migration...")
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(events)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"📊 Current columns: {columns}")
        
        # Add event_start column if it doesn't exist
        if 'event_start' not in columns:
            print("➕ Adding event_start column...")
            cursor.execute("ALTER TABLE events ADD COLUMN event_start TEXT")
            print("✅ event_start column added successfully!")
        else:
            print("ℹ️  event_start column already exists")
        
        # Add event_end column if it doesn't exist
        if 'event_end' not in columns:
            print("➕ Adding event_end column...")
            cursor.execute("ALTER TABLE events ADD COLUMN event_end TEXT")
            print("✅ event_end column added successfully!")
        else:
            print("ℹ️  event_end column already exists")
        
        # Commit changes
        conn.commit()
        
        # Verify the changes
        cursor.execute("PRAGMA table_info(events)")
        updated_columns = [column[1] for column in cursor.fetchall()]
        print(f"📊 Updated columns: {updated_columns}")
        
        # Check if both new columns are present
        if 'event_start' in updated_columns and 'event_end' in updated_columns:
            print("✅ Migration completed successfully!")
            return True
        else:
            print("❌ Migration failed - new columns not found")
            return False
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    """Run the migration"""
    print("=== Database Migration: Add Event Times ===\n")
    
    success = asyncio.run(migrate_database())
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("The events table now has event_start and event_end columns.")
        print("You can now use these fields when creating or updating events.")
    else:
        print("\n💥 Migration failed!")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main() 