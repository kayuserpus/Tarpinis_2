#!/bin/bash

# Navigate to the application directory
cd /home/site/wwwroot

# Run database migrations
flask db upgrade

# Initialize admin user
python -c "from app import init_admin_user; init_admin_user()"

# Start the application
flask run --host=0.0.0.0 --port=8000
