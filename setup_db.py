#!/usr/bin/env python3
"""
Database setup and migration script for Art Marketplace
"""

import os
import sys
from flask import Flask
from app import create_app, db
from app.models import (
    User, Category, Artwork, Order, OrderItem, ShippingTracking,
    Review, WishlistItem, ArtistProfile, Notification
)

def create_database():
    """Create database tables"""
    print("Creating database tables...")
    try:
        # Test database connection first
        db.engine.execute('SELECT 1')
        print("✓ Database connection successful")

        db.create_all()
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False
    return True

def seed_initial_data():
    """Seed initial data"""
    print("Seeding initial data...")

    try:
        # Create categories
        categories = [
            Category(name='Painting', description='Traditional and contemporary paintings'),
            Category(name='Sculpture', description='3D art pieces and sculptures'),
            Category(name='Photography', description='Artistic photography'),
            Category(name='Digital Art', description='Digital and computer-generated art'),
            Category(name='Mixed Media', description='Art combining multiple mediums')
        ]

        for category in categories:
            if not Category.query.filter_by(name=category.name).first():
                db.session.add(category)

        # Create admin user
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@artmarketplace.com')
        if not User.query.filter_by(email=admin_email).first():
            admin = User(
                email=admin_email,
                full_name='System Administrator',
                role='admin'
            )
            admin.set_password(os.environ.get('ADMIN_PASSWORD', 'admin123'))
            db.session.add(admin)

        db.session.commit()
        print("✓ Initial data seeded successfully")

    except Exception as e:
        print(f"✗ Error seeding data: {e}")
        db.session.rollback()
        return False
    return True

def run_migrations():
    """Run database migrations"""
    print("Running migrations...")
    try:
        # For now, just recreate tables (in production, use proper migration tools)
        db.create_all()
        print("✓ Migrations completed successfully")
    except Exception as e:
        print(f"✗ Error running migrations: {e}")
        return False
    return True

def main():
    """Main setup function"""
    print("Art Marketplace Database Setup")
    print("=" * 40)

    # Create Flask app
    app = create_app()

    with app.app_context():
        # Test database connection
        try:
            db.engine.execute('SELECT 1')
            print("✓ Database connection successful")
        except Exception as e:
            print(f"✗ Database connection failed: {e}")
            print("Please check your DATABASE_URL in .env file")
            sys.exit(1)

        # Create tables
        if not create_database():
            sys.exit(1)

        # Seed data
        if not seed_initial_data():
            sys.exit(1)

        # Run migrations
        if not run_migrations():
            sys.exit(1)

    print("\n✓ Database setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the Flask app: python run.py")
    print("2. Test the API endpoints")
    print("3. Start the frontend development server")

if __name__ == '__main__':
    main()