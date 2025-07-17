#!/usr/bin/env python3
"""
Initialize the database with the first admin user.
"""
import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sqlalchemy as sa
from sqlalchemy.orm import Session

from src.gpt_computer_agent.db.session import engine, Base
from src.gpt_computer_agent.models.user import User
from src.gpt_computer_agent.core.security import get_password_hash
from src.gpt_computer_agent.config.settings import settings

def init_db():
    """Initialize the database with required tables and first admin user."""
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = Session(bind=engine)
    
    try:
        # Check if admin user already exists
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            print("Creating admin user...")
            # Create admin user
            admin = User(
                username="admin",
                email=settings.FIRST_SUPERUSER,
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                full_name="Admin User",
                is_active=True,
                is_superuser=True
            )
            db.add(admin)
            db.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization complete!")
