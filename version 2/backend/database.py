#!/usr/bin/env python3

import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Product, Employee, Delivery
from datetime import date

def init_db():
    """Initialize the database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Create default admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@stockmaster.com')
            admin.set_password('1234')
            db.session.add(admin)
            print("✅ Created admin user (username: admin, password: 1234)")
        
        # Create sample products
        if Product.query.count() == 0:
            sample_products = [
                Product(id='PROD-0001', name='Laptop Dell XPS 13', qty=15, price=1299.99, 
                       threshold=5, date_added=date(2024, 1, 15)),
                Product(id='PROD-0002', name='Wireless Mouse', qty=50, price=29.99, 
                       threshold=10, date_added=date(2024, 1, 10)),
                Product(id='PROD-0003', name='Mechanical Keyboard', qty=25, price=89.99, 
                       threshold=5, date_added=date(2024, 1, 20)),
                Product(id='PROD-0004', name='27-inch Monitor', qty=8, price=299.99, 
                       threshold=3, date_added=date(2024, 2, 1)),
            ]
            db.session.bulk_save_objects(sample_products)
            print("✅ Created sample products")
        
        # Create sample employees
        if Employee.query.count() == 0:
            sample_employees = [
                Employee(id='EMPL-0001', name='John Smith', position='Warehouse Manager', 
                        department='Logistics', contact='john.smith@company.com'),
                Employee(id='EMPL-0002', name='Maria Garcia', position='Inventory Specialist', 
                        department='Operations', contact='maria.garcia@company.com'),
                Employee(id='EMPL-0003', name='David Chen', position='Delivery Coordinator', 
                        department='Shipping', contact='david.chen@company.com'),
            ]
            db.session.bulk_save_objects(sample_employees)
            print("✅ Created sample employees")
        
        db.session.commit()
        print("🎉 Database initialization completed successfully!")
        print("\n📊 Sample data created:")
        print(f"   - Users: {User.query.count()}")
        print(f"   - Products: {Product.query.count()}")
        print(f"   - Employees: {Employee.query.count()}")

def reset_db():
    """Reset the database (drop and recreate)"""
    app = create_app()
    
    with app.app_context():
        print("⚠️  Resetting database...")
        db.drop_all()
        db.create_all()
        print("✅ Database reset completed")
        init_db()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        reset_db()
    else:
        init_db()