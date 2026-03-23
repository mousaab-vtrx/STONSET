"""
FastAPI application entry point.
Main application factory with middleware, exception handlers, and router registration.
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1 import (
    auth, users, departments, niveaux, filieres, modules, sections,
    groupes_tp, etats, creneaux, vacances, systemes, logiciels,
    salles_tp, reservations, management, avatars, account
)
from app.core.config import settings
from app.core.exceptions import ApplicationError
from app.core.logging import logger
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Initialize database
    from app.db.session import init_db
    try:
        await init_db()
        logger.info("✓ Database initialized")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Clean Architecture API Scaffold - Domain-Driven Design",
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware BEFORE any routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # React frontend (primary)
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://host.docker.internal:3000",
        "http://host.docker.internal:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)


# Exception handlers
@app.exception_handler(ApplicationError)
async def app_exception_handler(request: Request, exc: ApplicationError):
    """Handle custom app exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "data": None,
            "message": exc.message,
            "errors": None,
            "meta": None,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    errors = {}
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"][1:])
        errors[field] = error["msg"]
    
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "data": None,
            "message": "Validation error",
            "errors": errors,
            "meta": None,
        },
    )


# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(avatars.router)
app.include_router(management.router)
app.include_router(account.router, prefix="/api/v1")

# Domain entity routers
app.include_router(departments.router, prefix="/api/v1")
app.include_router(niveaux.router, prefix="/api/v1")
app.include_router(filieres.router, prefix="/api/v1")
app.include_router(modules.router, prefix="/api/v1")
app.include_router(sections.router, prefix="/api/v1")
app.include_router(groupes_tp.router, prefix="/api/v1")
app.include_router(etats.router, prefix="/api/v1")
app.include_router(creneaux.router, prefix="/api/v1")
app.include_router(vacances.router, prefix="/api/v1")
app.include_router(systemes.router, prefix="/api/v1")
app.include_router(logiciels.router, prefix="/api/v1")
app.include_router(salles_tp.router, prefix="/api/v1")
app.include_router(reservations.router, prefix="/api/v1")


# Serve static files (uploads folder)
uploads_dir = Path(__file__).parent.parent / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.APP_VERSION}


# Root endpoint
@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "api_docs": "/docs",
        "openapi_schema": "/openapi.json",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )

