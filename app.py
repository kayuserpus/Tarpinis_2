import os
from app import create_app

# Check if the environment variables are set, if not, set them
if not os.getenv('ADMIN_USERNAME'):
    os.environ['ADMIN_USERNAME'] = 'default_admin_username'
if not os.getenv('ADMIN_EMAIL'):
    os.environ['ADMIN_EMAIL'] = 'default_admin_email@example.com'
if not os.getenv('ADMIN_PASSWORD'):
    os.environ['ADMIN_PASSWORD'] = 'default_admin_password'

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
