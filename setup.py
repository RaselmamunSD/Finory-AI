"""
Setup script for Finory IA
"""
import os
import sys

def setup_project():
    """Setup the Django project"""
    print("Setting up Finory IA...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("""# Django Settings
SECRET_KEY=django-insecure-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Celery (Redis)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Encryption
ENCRYPTION_KEY=dev-encryption-key-change-in-production

# AI Settings
AI_ENABLED=True
AI_AUTONOMOUS_MODE_DEFAULT=False
""")
        print(".env file created!")
    
    # Create logs directory
    if not os.path.exists('logs'):
        os.makedirs('logs')
        print("logs directory created!")
    
    # Create media and static directories
    for directory in ['media', 'static']:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"{directory} directory created!")
    
    print("\nSetup complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run migrations: python manage.py makemigrations")
    print("3. Apply migrations: python manage.py migrate")
    print("4. Create superuser: python manage.py createsuperuser")
    print("5. Run server: python manage.py runserver")

if __name__ == '__main__':
    setup_project()
