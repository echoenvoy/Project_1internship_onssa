#!/usr/bin/env python3

import os
import subprocess
import sys

def run_command(command, description):
    print(f"🚀 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ {description} failed: {result.stderr}")
            return False
        print(f"✅ {description} completed successfully!")
        return True
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("📦 Stock Manager Setup Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('backend'):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if Python is installed
    if not run_command("python --version", "Checking Python installation"):
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("⚠️  Trying alternative approach...")
        run_command("python -m pip install -r requirements.txt", "Installing with python -m pip")
    
    # Create necessary directories
    directories = ['logs', 'backups']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    print("\n📋 Setup completed! Next steps:")
    print("1. Make sure PostgreSQL is running")
    print("2. Run: python backend/database.py")
    print("3. Run: python backend/app.py")
    print("4. Open: http://localhost:5000")

if __name__ == "__main__":
    main()