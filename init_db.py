#!/usr/bin/env python3
"""
Database initialization script.
Creates all tables based on SQLModel models.
Run from: cd backend && python ../init_db.py
"""
import asyncio
import sys
import os
from pathlib import Path

# Set working directory to backend
backend_dir = Path(__file__).parent / "backend"
os.chdir(backend_dir)
sys.path.insert(0, str(backend_dir))

async def init_db():
    """Initialize database and create all tables."""
    from app.db.session import engine
    from sqlmodel import SQLModel
    # Import all models to ensure they're registered
    from app.models import (
        User, Department, Niveau, Filiere, Module, Section,
        GroupeTP, Etat, Creneau, Vacances, Systeme, Logiciel,
        SalleTP, Reservation
    )
    
    print("🔧 Creating database tables...")
    
    try:
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        print("✅ Database tables created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
