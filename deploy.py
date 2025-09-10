#!/usr/bin/env python3
"""
Production deployment script for Personal Budgeting API

This script helps automate common deployment tasks:
- Collect static files
- Run database migrations
- Create superuser (optional)
- Check system status
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_budgeting_api.settings')

# Initialize Django
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


def collect_static():
    """Collect static files for production"""
    print("Collecting static files...")
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✓ Static files collected successfully")
    except Exception as e:
        print(f"✗ Error collecting static files: {e}")
        return False
    return True


def run_migrations():
    """Run database migrations"""
    print("Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ Migrations completed successfully")
    except Exception as e:
        print(f"✗ Error running migrations: {e}")
        return False
    return True


def check_system():
    """Check system status"""
    print("Checking system status...")
    try:
        execute_from_command_line(['manage.py', 'check', '--deploy'])
        print("✓ System check passed")
    except Exception as e:
        print(f"✗ System check failed: {e}")
        return False
    return True


def create_superuser():
    """Create a superuser account"""
    print("Creating superuser account...")
    try:
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            print("✓ Superuser already exists")
            return True
        
        # Create superuser with environment variables or defaults
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass123')
        
        User.objects.create_superuser(username, email, password)
        print(f"✓ Superuser '{username}' created successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating superuser: {e}")
        return False


def main():
    """Main deployment function"""
    print("🚀 Starting Personal Budgeting API deployment...")
    print("=" * 50)
    
    # Check if we're in production mode
    if settings.DEBUG:
        print("⚠️  Warning: Running in DEBUG mode")
        response = input("Continue with deployment? (y/N): ")
        if response.lower() != 'y':
            print("Deployment cancelled")
            return
    
    # Run deployment steps
    steps = [
        ("System Check", check_system),
        ("Database Migrations", run_migrations),
        ("Static Files Collection", collect_static),
        ("Superuser Creation", create_superuser),
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if step_func():
            success_count += 1
        else:
            print(f"❌ {step_name} failed")
    
    print("\n" + "=" * 50)
    if success_count == len(steps):
        print("🎉 Deployment completed successfully!")
        print("\nNext steps:")
        print("1. Configure your web server (nginx, Apache)")
        print("2. Set up SSL certificates")
        print("3. Configure your database")
        print("4. Set up monitoring and logging")
        print("5. Test your API endpoints")
    else:
        print(f"⚠️  Deployment completed with {len(steps) - success_count} failures")
        print("Please review the errors above and fix them before proceeding")


if __name__ == '__main__':
    main()

