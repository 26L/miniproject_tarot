from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import readings

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

    # Mount Static Files
    _app.mount("/static", StaticFiles(directory="static"), name="static")

    # Include Routers
    _app.include_router(readings.router, prefix="/api/reading", tags=["Reading"])

    @_app.get("/")
    async def root():
        return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

    @_app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return _app

app = get_application()
