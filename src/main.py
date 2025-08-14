from fastapi import FastAPI
from .database import Base, engine
from .credits import router as credits_router, schema_router
from .tasks import start_scheduler, shutdown_scheduler

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LawVriksh Credit Management API",
    description="Tracks and manages user credits with add/deduct/reset and daily auto-credit features.",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    shutdown_scheduler()

@app.get("/")
def root():
    return {
        "message": "Welcome to the LawVriksh Credit Management API!",
        "docs_url": "/docs",
        "health_url": "/api/health"
    }

# Register routers
app.include_router(credits_router)   # All /api/credits endpoints
app.include_router(schema_router)    # /api/schema/update
