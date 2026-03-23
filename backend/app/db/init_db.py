"""
Database initialization script.
Run this to create all tables.
"""
import asyncio

# Import all models to ensure they're registered
from app.models import (  # noqa: F401
    User, Department, Niveau, Filiere, Module, Section,
    GroupeTP, Etat, Creneau, Vacances, Systeme, Logiciel,
    SalleTP, Reservation, AccountDeletionFeedback
)
from app.db.session import init_db


async def main() -> None:
    """Initialize database."""
    print("Creating database tables...")
    await init_db()
    print("✓ Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(main())
