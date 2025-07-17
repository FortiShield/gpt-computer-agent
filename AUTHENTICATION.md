# Authentication System

This document provides an overview of the authentication system implemented in the GPT Computer Agent.

## Features

- JWT-based authentication
- User registration and login
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Refresh token support
- Secure password reset flow
- API key authentication for programmatic access

## Setup

1. Install the required dependencies:

```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

2. Set up your environment variables in `.env`:

```env
# Authentication
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS=30
JWT_ALGORITHM=HS256
JWT_ISSUER=gpt-computer-agent

# First superuser (created on first run if no users exist)
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=changeme
```

3. Run the database migrations:

```bash
alembic upgrade head
```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/token` - Login and get access token
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password with token

### Users

- `GET /api/users/me` - Get current user info
- `PUT /api/users/me` - Update current user
- `GET /api/users/` - List all users (admin only)
- `GET /api/users/{user_id}` - Get user by ID
- `PUT /api/users/{user_id}` - Update user (admin or self)
- `DELETE /api/users/{user_id}` - Delete user (admin only)

## Usage

### Register a new user

```bash
curl -X 'POST' \
  'http://localhost:8000/api/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "user@example.com",
    "username": "user",
    "password": "string",
    "full_name": "string"
  }'
```

### Login

```bash
curl -X 'POST' \
  'http://localhost:8000/api/auth/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=user%40example.com&password=string&scope=&client_id=&client_secret='
```

### Make authenticated request

```bash
curl -X 'GET' \
  'http://localhost:8000/api/users/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

## Security Considerations

- Always use HTTPS in production
- Store secrets in environment variables, never in code
- Set appropriate CORS policies
- Implement rate limiting
- Use secure, random secret keys
- Keep dependencies updated
- Regularly rotate secrets

## Testing

To run the test suite:

```bash
pytest tests/
```

## License

This authentication system is part of the GPT Computer Agent project and is licensed under the MIT License.
