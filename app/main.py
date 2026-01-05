from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging_config import setup_logging, get_logger
from app.api.routers import readings, interpretations

# Setup Logging
setup_logging()
logger = get_logger(__name__)

def get_application() -> FastAPI:
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        debug=settings.DEBUG
    )

    # Set all CORS enabled origins
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global Exception Handler
    @_app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Global Exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error", "details": str(exc) if settings.DEBUG else "An unexpected error occurred."}
        )

    # Mount Static Files
    _app.mount("/static", StaticFiles(directory="static"), name="static")

    # Include Routers
    _app.include_router(readings.router, prefix="/api/reading", tags=["Reading"])
    _app.include_router(interpretations.router, prefix="/api/reading", tags=["AI Interpretation"])

    @_app.get("/")
    async def root():
        logger.info("Root endpoint accessed")
        return {"message": f"Welcome to {settings.PROJECT_NAME} API v0.2"}

    @_app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return _app

app = get_application()
