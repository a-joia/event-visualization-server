import asyncio
from database import init_db
from config import settings
import os

async def main():
    """Initialize the database and create tables."""
    print("Initializing database...")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    # Check if database file exists
    db_file = settings.DATABASE_URL.replace('sqlite+aiosqlite:///', '')
    if os.path.exists(db_file):
        print(f"Database file exists: {db_file}")
    else:
        print(f"Database file will be created: {db_file}")
    
    try:
        await init_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 