import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_postgresql():
    try:
        # Get database URL from environment
        db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:1234@localhost:5432/stock_manager')
        
        print(f"Testing connection to: {db_url.split('@')[-1]}")
        
        # Try to connect
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print("✅ PostgreSQL Connection Successful!")
        print(f"📊 PostgreSQL Version: {version[0]}")
        
        # Check if database exists
        cursor.execute("SELECT datname FROM pg_database WHERE datname = 'stock_manager';")
        db_exists = cursor.fetchone()
        
        if db_exists:
            print("✅ Database 'stock_manager' exists")
        else:
            print("❌ Database 'stock_manager' does not exist")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ PostgreSQL Connection Failed: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your password in the DATABASE_URL")
        print("3. Verify the database 'stock_manager' exists")
        print("4. Check if port 5432 is open")

if __name__ == "__main__":
    test_postgresql()