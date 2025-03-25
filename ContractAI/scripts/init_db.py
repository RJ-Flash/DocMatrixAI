#!/usr/bin/env python
"""
Database initialization script for ContractAI.

This script creates the database tables and adds an admin user.
Run this script after setting up your environment:

python -m scripts.init_db

"""
import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import Base, engine, SessionLocal, User
from app.core.security import get_password_hash
from app.config import get_settings

settings = get_settings()


def init_db():
    """Initialize the database with tables and initial data."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
    
    # Check if admin user exists
    db = SessionLocal()
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    
    if not admin_user:
        print("Creating admin user...")
        admin_user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin"),
            full_name="Admin User",
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")
    
    db.close()


def create_buckets():
    """Create required Minio buckets."""
    try:
        from minio import Minio
        from minio.error import S3Error
        
        print("Connecting to Minio...")
        client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        
        # Create document bucket if it doesn't exist
        if not client.bucket_exists(settings.DOCUMENT_BUCKET):
            print(f"Creating bucket: {settings.DOCUMENT_BUCKET}")
            client.make_bucket(settings.DOCUMENT_BUCKET)
        else:
            print(f"Bucket already exists: {settings.DOCUMENT_BUCKET}")
        
        # Create processed documents bucket if it doesn't exist
        if not client.bucket_exists(settings.PROCESSED_BUCKET):
            print(f"Creating bucket: {settings.PROCESSED_BUCKET}")
            client.make_bucket(settings.PROCESSED_BUCKET)
        else:
            print(f"Bucket already exists: {settings.PROCESSED_BUCKET}")
            
        print("Minio buckets setup completed.")
        
    except S3Error as e:
        print(f"Error setting up Minio buckets: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    print("Initializing ContractAI database...")
    init_db()
    
    print("\nSetting up storage buckets...")
    create_buckets()
    
    print("\nInitialization complete!")
    print("\nYou can now run the application with:")
    print("    uvicorn app.main:app --reload")
    print("\nDefault admin credentials:")
    print("    Email: admin@example.com")
    print("    Password: admin")
    print("\nIMPORTANT: Change the admin password after first login!") 