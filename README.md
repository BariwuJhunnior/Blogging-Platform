# Blogging Platform API

A robust and feature-rich REST API built with Django and Django REST Framework for managing blog posts, categories, tags, users, and social interactions. This API provides a complete backend solution for a blogging platform with authentication, authorization, search capabilities, real-time notifications, and comprehensive documentation.

## Features

### Core Functionality

- **User Management**: Registration, authentication, profile management (bio, location, profile picture), and user following
- **Post Management**: Full CRUD operations for blog posts with draft/published workflow, automatic publishing timestamps
- **Comments**: Comment system for posts with full CRUD operations
- **Engagement**: Like/unlike posts, rate posts (1-5 stars), view top-rated posts
- **Categorization**: Organize posts with categories and tags, category subscriptions for personalized feeds
- **Feeds**: Personalized user feed (followed authors + subscribed categories), global discovery feed
- **Search & Filtering**: Advanced search and filtering capabilities across posts, authors, categories, and tags
- **Authorization**: Role-based permissions (authors can only edit their own posts/comments)
- **Social Sharing**: Share posts via email with background task processing
- **Notifications**: Email notifications for new posts to followers and category subscribers, 5-star rating alerts
- **API Documentation**: Interactive API documentation with Swagger and Redoc

### Technical Features

- **Token-based Authentication**: Secure API access using Django REST Framework tokens
- **Auto-generated Documentation**: Interactive API docs using drf-spectacular
- **Database Optimization**: Efficient queries with proper relationships and select_related/prefetch_related
- **Input Validation**: Comprehensive data validation and error handling
- **Async Tasks**: Background email processing using Celery and Redis
- **Media Handling**: Profile picture uploads with Pillow
- **Testing**: Extensive test coverage with unit and integration tests
- **Pagination**: Page-based pagination for large result sets
- **Caching**: Optimized for performance with database indexing

## Requirements

- Python 3.8+
- Django 4.2+
- Django REST Framework 3.14+
- MySQL 5.7+
- Redis (for Celery background tasks)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd blogging-platform-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and start Redis

Ensure Redis is installed and running on your system (default localhost:6379).

On Ubuntu/Debian:

```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
```

On macOS:

```bash
brew install redis
brew services start redis
```

On Windows: Download from https://redis.io/download and run redis-server.exe

### 5. Database Setup

Ensure you have MySQL installed and create a database:

```sql
CREATE DATABASE blogging_platform_api_db;
```

### 6. Configure environment

Update the database configuration in `blogging_platform_api/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blogging_platform_api_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
```

### 7. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 9. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

### 10. Run Celery Worker (for background tasks)

In a separate terminal (with virtual environment activated):

```bash
celery -A blogging_platform_api worker --loglevel=info
```

For production, you may want to run Celery with a process manager like Supervisor.

## API Documentation

### Interactive Documentation

- **Swagger UI**: `http://127.0.0.1:8000/api/docs/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/api/docs/redoc/`
- **Schema**: `http://127.0.0.1:8000/api/schema/`

### API Endpoints

#### Authentication Endpoints

| Method | Endpoint                           | Description         | Authentication |
| ------ | ---------------------------------- | ------------------- | -------------- |
| POST   | `/api/register/`                   | User registration   | None           |
| POST   | `/api/login/`                      | User login          | None           |
| GET    | `/api/profile/`                    | Get current profile | Token Required |
| GET    | `/api/profiles/<username>/`        | Get user profile    | None           |
| POST   | `/api/profiles/<username>/follow/` | Follow user         | Token Required |
| GET    | `/api/users/`                      | List users          | None           |

#### Post Management Endpoints

| Method | Endpoint                   | Description         | Authentication   |
| ------ | -------------------------- | ------------------- | ---------------- |
| GET    | `/api/posts/`              | List all posts      | None             |
| POST   | `/api/posts/`              | Create new post     | Token Required   |
| GET    | `/api/posts/<id>/`         | Get post details    | None             |
| PUT    | `/api/posts/<id>/`         | Update post         | Token Required\* |
| PATCH  | `/api/posts/<id>/`         | Partial update post | Token Required\* |
| DELETE | `/api/posts/<id>/`         | Delete post         | Token Required\* |
| POST   | `/api/posts/<id>/publish/` | Publish draft post  | Token Required\* |

\*Only the author of the post can modify or delete it.

#### Comment Endpoints

| Method | Endpoint                         | Description            | Authentication   |
| ------ | -------------------------------- | ---------------------- | ---------------- |
| GET    | `/api/posts/<post_id>/comments/` | List comments          | None             |
| POST   | `/api/posts/<post_id>/comments/` | Create comment         | Token Required   |
| GET    | `/api/comments/<id>/`            | Get comment details    | None             |
| PUT    | `/api/comments/<id>/`            | Update comment         | Token Required\* |
| PATCH  | `/api/comments/<id>/`            | Partial update comment | Token Required\* |
| DELETE | `/api/comments/<id>/`            | Delete comment         | Token Required\* |

\*Only the author of the comment can modify or delete it.

#### Engagement Endpoints

| Method | Endpoint                 | Description          | Authentication |
| ------ | ------------------------ | -------------------- | -------------- |
| POST   | `/api/posts/<id>/like/`  | Like/unlike post     | Token Required |
| POST   | `/api/posts/<id>/rate/`  | Rate post (1-5)      | Token Required |
| GET    | `/api/posts/top/`        | Get top-rated posts  | None           |
| POST   | `/api/posts/<id>/share/` | Share post via email | Token Required |

#### Category Endpoints

| Method | Endpoint                          | Description           | Authentication |
| ------ | --------------------------------- | --------------------- | -------------- |
| GET    | `/api/categories/`                | List categories       | None           |
| POST   | `/api/categories/<id>/subscribe/` | Subscribe to category | Token Required |
| GET    | `/api/categories/<name>/posts/`   | Posts in category     | None           |

#### Feed Endpoints

| Method | Endpoint        | Description           | Authentication |
| ------ | --------------- | --------------------- | -------------- |
| GET    | `/api/feed/`    | Personalized feed     | Token Required |
| GET    | `/api/explore/` | Global discovery feed | None           |
| GET    | `/api/drafts/`  | User's draft posts    | Token Required |

## Search & Filtering

The API supports advanced search and filtering capabilities:

### Search Parameters

- `search`: Search in post titles, content, author username, and tag names
- `category`: Filter by category name
- `author`: Filter by author username
- `tags`: Filter by tag name
- `published_date`: Filter by specific publication date
- `published_after`: Filter posts published after the date
- `published_before`: Filter posts published before the date

### Example Requests

```bash
# Search posts
GET /api/posts/?search=django

# Filter by category
GET /api/posts/?category=Technology

# Filter by author
GET /api/posts/?author=johndoe

# Filter by multiple criteria
GET /api/posts/?category=Tech&author=johndoe&search=tutorial

# Date range filtering
GET /api/posts/?published_after=2024-01-01&published_before=2024-12-31
```

## Authentication

The API uses token-based authentication. To access protected endpoints:

1. **Register or Login** to obtain a token
2. **Include the token** in request headers:
   ```
   Authorization: Token your_token_here
   ```

### Example Authentication Flow

#### 1. Register a new user

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword"
  }'
```

#### 2. Log in to get a token

```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword"
  }'
```

#### 3. Use a token for authenticated requests

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your_token_here" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my blog post.",
    "category_name": "Technology",
    "tags": ["python", "django", "tutorial"]
  }'
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report

# Run specific test file
python manage.py test posts.tests.PostTests
```

### Test Coverage

The project includes extensive tests covering:

- User authentication and registration
- Post CRUD operations
- Permission enforcement
- Search and filtering functionality
- Input validation and error handling

## Project Structure

```
blogging_platform_api/
├── manage.py
├── requirements.txt
├── .gitignore
├── .coverage
├── .coveragerc
├── blogging_platform_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── celery.py
├── posts/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── filters.py
│   ├── tests.py
│   ├── tasks.py
│   ├── utils.py
│   ├── signals.py
│   └── migrations/
├── users/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── signals.py
│   ├── tests.py
│   └── migrations/
└── media/
    └── profile_pics/
```

### Key Components

#### Models

- **User**: Django's built-in user model with profile extension
- **Profile**: User profile with bio, location, and profile picture
- **Follow**: User following relationships
- **Category**: Blog post categories
- **Tag**: Reusable tags for posts
- **Post**: Main blog post model with relationships to User, Category, and Tags
- **Comment**: Comments on posts
- **Like**: User likes on posts
- **Rating**: User ratings (1-5 stars) on posts
- **CategorySubscription**: User subscriptions to categories

#### Views & Serializers

- **Generic Views**: Using Django REST Framework's class-based views
- **Custom Serializers**: Custom field handling for better API experience
- **Permission Classes**: Custom permission implementation for post ownership
- **Background Tasks**: Celery tasks for email notifications and sharing

#### Features

- **Filtering**: Django Filter integration for advanced querying
- **Search**: Full-text search across multiple fields
- **Documentation**: Automatic API documentation generation
- **Validation**: Comprehensive input validation and error handling
- **Notifications**: Email notifications via Celery tasks

## Deployment

### Production Settings

1. Set `DEBUG = False` in `settings.py`
2. Configure proper `SECRET_KEY`
3. Set appropriate `ALLOWED_HOSTS`
4. Use environment variables for sensitive data
5. Configure proper database settings
6. Set up static file serving
7. Configure email backend for production

### Example Production Configuration

```python
import os
from pathlib import Path

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

### Docker Deployment

Create a `Dockerfile` for containerized deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Running Celery in Production

Use a process manager like Supervisor or systemd to run the Celery worker:

```ini
# supervisor config example
[program:celery]
command=/path/to/env/bin/celery -A blogging_platform_api worker --loglevel=info
directory=/path/to/project
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Use meaningful commit messages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [API Documentation](http://127.0.0.1:8000/api/docs/swagger/)
2. Review the test files for usage examples
3. Create an issue on GitHub

---

**Built using Django and Django REST Framework**
**Built as capstone project**
