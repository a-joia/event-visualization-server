from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database_manager import db_manager
from apis.events import router as events_router
from config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Include routers
app.include_router(events_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    success = await db_manager.init_database()
    if not success:
        raise Exception("Failed to initialize database")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    await db_manager.close()

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "API is running"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": settings.API_TITLE,
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/api/health"
    }

