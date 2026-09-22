from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.security import get_password_hash
from app.api.endpoints import chat, admin, upload # type: ignore
from app.database import Base, SessionLocal, engine
from app.models import models  # noqa: F401


def ensure_default_users(db):
    default_users = [
        {
            "email": "admin@eubia.de",
            "full_name": "Administrateur EUBIA",
            "password": "EUBIA-Admin-2026!",
            "role": "admin",
        },
        {
            "email": "hr@eubia.de",
            "full_name": "HR EUBIA",
            "password": "EUBIA-HR-2026!",
            "role": "hr",
        },
        {
            "email": "employee@eubia.de",
            "full_name": "Collaborateur EUBIA",
            "password": "EUBIA-User-2026!",
            "role": "user",
        },
    ]

    for user_data in default_users:
        existing = db.query(models.User).filter(models.User.email == user_data["email"]).first()
        if existing:
            if existing.role != user_data["role"]:
                existing.role = user_data["role"]
            if not existing.hashed_password:
                existing.hashed_password = get_password_hash(user_data["password"])
            if not existing.is_active:
                existing.is_active = True
            continue

        db.add(
            models.User(
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash(user_data["password"]),
                is_active=True,
                role=user_data["role"],
            )
        )

    db.commit()


app = FastAPI(
    title="RH Assistant API",
    description="API for the Smart HR Assistant",
    version="0.1.0",
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
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


@app.on_event("startup")
async def startup_event():
    # The legacy schema contains PostgreSQL-only types; bootstrap only the
    # tables used by the current EUBIA flow in local SQLite mode.
    Base.metadata.create_all(
        bind=engine,
        tables=[
            models.User.__table__,
            models.DocumentRecord.__table__,
            models.HRQuestion.__table__,
        ],
    )

    with SessionLocal() as db:
        ensure_default_users(db)


@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the EUBIA HR Assistant API"}


@app.get("/health", tags=["root"])
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME}
