from fastapi import FastAPI
from .routes import alerts, auth, metrics, users

def create_app() -> FastAPI:
    app = FastAPI(title="VOC Analytics API")
    
    # Include routers
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
    app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
    
    return app