from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import Settings
from core.database import Database
from .routes import alerts, auth, metrics, users
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    # Initialize settings
    settings = Settings()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="VOC Analytics API"
    )
    
    # Setup CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(
        auth.router,
        prefix=f"{settings.API_PREFIX}/auth",
        tags=["Authentication"]
    )
    app.include_router(
        users.router,
        prefix=f"{settings.API_PREFIX}/users",
        tags=["Users"]
    )
    app.include_router(
        alerts.router,
        prefix=f"{settings.API_PREFIX}/alerts",
        tags=["Alerts"]
    )
    app.include_router(
        metrics.router,
        prefix=f"{settings.API_PREFIX}/metrics",
        tags=["Metrics"]
    )
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize services on startup"""
        logger.info("Initializing services...")
        
        # Initialize database
        database = Database(settings)
        await database.init_db()
        
        # Initialize other services
        # Add other initialization code here
        
        logger.info("Services initialized successfully")
        
    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown"""
        logger.info("Shutting down services...")
        
        # Cleanup code here
        
        logger.info("Shutdown complete")
        
    return app

# Create app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)