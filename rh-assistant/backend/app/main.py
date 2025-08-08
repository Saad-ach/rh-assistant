from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.endpoints import chat, admin, upload # type: ignore

app = FastAPI(
    title="RH Assistant API",
    description="API for the Smart HR Assistant",
    version="0.1.0",
)

# Configure CORS
origins = [
    "http://localhost:3000",  # React frontend
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])


@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the RH Assistant API"}
