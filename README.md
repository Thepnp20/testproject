# FastAPI Celery MongoDB Demo

A comprehensive FastAPI application with Celery background workers and MongoDB using Beanie ODM.

## Features

- **FastAPI**: Modern, fast web framework with automatic API documentation
- **Celery**: Distributed task queue for background job processing
- **MongoDB**: NoSQL database with Beanie ODM for async operations
- **Redis**: Message broker for Celery tasks
- **Task Management**: Complete CRUD operations with status tracking
- **User Management**: User registration and management
- **Task Logs**: Detailed execution logs for background tasks
- **Statistics**: Real-time task and user statistics
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

## Prerequisites

- Python 3.8+
- MongoDB (running on localhost:27017)
- Redis (running on localhost:6379)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd railway
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your configuration
   ```

## Running the Application

### 1. Start MongoDB
```bash
# Make sure MongoDB is running on localhost:27017
mongod
```

### 2. Start Redis
```bash
# Make sure Redis is running on localhost:6379
redis-server
```

### 3. Start Celery Worker
```bash
# In a new terminal
celery -A celery_worker.celery_app worker --loglevel=info
```

### 4. Start FastAPI Application
```bash
# In another terminal
python run.py
```

The application will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Tasks
- `POST /tasks/` - Create a new task
- `GET /tasks/` - List tasks with filtering
- `GET /tasks/{task_id}` - Get specific task
- `GET /tasks/{task_id}/with-logs` - Get task with execution logs
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task
- `POST /tasks/{task_id}/process` - Start task processing
- `GET /tasks/{task_id}/celery-status` - Get Celery task status
- `POST /tasks/cleanup` - Clean up old tasks
- `POST /tasks/generate-report` - Generate reports
- `GET /tasks/stats/summary` - Get task statistics

### Users
- `POST /users/` - Create a new user
- `GET /users/` - List users with filtering
- `GET /users/{user_id}` - Get specific user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user
- `GET /users/stats/summary` - Get user statistics

## Usage Examples

### Creating and Processing Tasks

1. **Create a task**
   ```bash
   curl -X POST "http://localhost:8000/tasks/" \
        -H "Content-Type: application/json" \
        -d '{
          "title": "Data Processing Task",
          "description": "Process user data for analytics",
          "priority": "high"
        }'
   ```

2. **Start task processing**
   ```bash
   curl -X POST "http://localhost:8000/tasks/{task_id}/process?operation=data_processing"
   ```

3. **Check task status**
   ```bash
   curl -X GET "http://localhost:8000/tasks/{task_id}/celery-status"
   ```

4. **Get task with logs**
   ```bash
   curl -X GET "http://localhost:8000/tasks/{task_id}/with-logs"
   ```

### User Management

1. **Create a user**
   ```bash
   curl -X POST "http://localhost:8000/users/" \
        -H "Content-Type: application/json" \
        -d '{
          "username": "john_doe",
          "email": "john@example.com",
          "full_name": "John Doe"
        }'
   ```

2. **List users**
   ```bash
   curl -X GET "http://localhost:8000/users/?limit=10&skip=0"
   ```

### Statistics and Reports

1. **Get task statistics**
   ```bash
   curl -X GET "http://localhost:8000/tasks/stats/summary"
   ```

2. **Generate a report**
   ```bash
   curl -X POST "http://localhost:8000/tasks/generate-report?report_type=daily"
   ```

## Background Task Operations

The application supports several types of background operations:

- **Data Processing**: Simulates data transformation and analytics
- **File Processing**: Simulates file operations (validation, conversion, compression)
- **Email Sending**: Simulates email campaign processing
- **Default Processing**: Generic task processing

Each operation includes:
- Progress logging
- Error handling
- Status updates
- Result storage

## Configuration

Edit the `.env` file to customize:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=fastapi_celery_demo

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true
```

## Development

### Project Structure
```
railway/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database initialization
│   ├── models.py            # Beanie models
│   ├── schemas.py           # Pydantic schemas
│   ├── celery_app.py        # Celery configuration
│   ├── tasks.py             # Background tasks
│   └── api/
│       ├── __init__.py
│       ├── tasks.py         # Task API routes
│       └── users.py         # User API routes
├── requirements.txt
├── run.py                   # Application runner
├── celery_worker.py         # Celery worker
├── env.example
└── README.md
```

### Adding New Tasks

1. **Define the task in `app/tasks.py`**
   ```python
   @celery_app.task(bind=True)
   def my_new_task(self, param1: str, param2: int):
       # Task implementation
       pass
   ```

2. **Add API endpoint in `app/api/tasks.py`**
   ```python
   @router.post("/my-new-task")
   async def start_my_task(param1: str, param2: int):
       celery_task = my_new_task.delay(param1, param2)
       return {"task_id": celery_task.id}
   ```

## Monitoring

- **Celery Flower**: Monitor Celery tasks at http://localhost:5555
  ```bash
  pip install flower
  celery -A celery_worker.celery_app flower
  ```

- **MongoDB Compass**: GUI for MongoDB management
- **Redis Commander**: Web interface for Redis
  ```bash
  npm install -g redis-commander
  redis-commander
  ```

## 🚀 Railway Deployment

This application is configured for **instant deployment** to Railway using configuration files with **separate services** for better scalability and reliability.

### Option 1: One-Click Deployment (Recommended)

The easiest way to deploy instantly:

```bash
# Run the instant deployment script
./deploy-instantly.sh
```

This script will automatically:
- ✅ Check all prerequisites
- ✅ Initialize Railway project
- ✅ Configure all services
- ✅ Deploy your application
- ✅ Test the deployment
- ✅ Provide you with the live URL

### Option 2: Railway Dashboard Deployment

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Add Railway deployment configuration"
   git push origin main
   ```

2. **Deploy via Railway Dashboard**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Railway will automatically detect the configuration files

### Option 3: Railway CLI Deployment

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Configuration Files

Your project includes essential configuration files:
- `railway.json` - Main Railway configuration with separate services
- `railway.toml` - Alternative configuration format
- `Dockerfile` - FastAPI application container
- `celery-worker.Dockerfile` - Celery worker container
- `celery-flower.Dockerfile` - Celery monitoring container

### Testing Your Deployment

```bash
# Set your app URL
export APP_URL=https://your-app-name.railway.app

# Test your deployment
./test-railway.sh

# Check Celery worker status
./check-celery.sh
```

### Services Architecture

Your Railway deployment includes **3 separate services**:

1. **FastAPI App** (`app` service)
   - Main web application
   - API endpoints and documentation
   - Health checks and monitoring

2. **Celery Worker** (`celery-worker` service)
   - Background task processing
   - Separate from web app for scalability
   - Automatic restart on failures

3. **Celery Flower** (`celery-flower` service)
   - Web-based monitoring for Celery
   - Real-time task monitoring
   - Worker status and statistics

## 📋 Prerequisites

1. **GitHub Repository**: Your code must be in a GitHub repository
2. **Railway Account**: Sign up at [railway.app](https://railway.app)
3. **Railway CLI** (optional): `npm install -g @railway/cli`

## 🔧 Configuration Details

### Build Configuration
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  }
}
```

### Deployment Configuration
```json
{
  "deploy": {
    "startCommand": "./railway-start.sh",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "numReplicas": 1
  }
}
```

### Environment Variables
```json
{
  "environment": {
    "MONGODB_URL": "mongodb://mongodb:27017",
    "DATABASE_NAME": "fastapi_celery_demo",
    "REDIS_URL": "redis://redis:6379/0",
    "CELERY_BROKER_URL": "redis://redis:6379/0",
    "CELERY_RESULT_BACKEND": "redis://redis:6379/0",
    "APP_HOST": "0.0.0.0",
    "APP_PORT": "8000",
    "DEBUG": "false"
  }
}
```



## Production Deployment

1. **Use production-grade servers**
   - Gunicorn with Uvicorn workers
   - Supervisor for process management

2. **Configure external services**
   - MongoDB Atlas or self-hosted MongoDB
   - Redis Cloud or self-hosted Redis

3. **Environment variables**
   - Set `DEBUG=false`
   - Configure proper CORS origins
   - Use strong passwords and authentication

4. **Security considerations**
   - Enable authentication/authorization
   - Use HTTPS
   - Implement rate limiting
   - Add input validation

## Troubleshooting

### Common Issues

1. **MongoDB connection failed**
   - Ensure MongoDB is running on localhost:27017
   - Check MongoDB authentication if enabled

2. **Redis connection failed**
   - Ensure Redis is running on localhost:6379
   - Check Redis authentication if enabled

3. **Celery tasks not processing**
   - Ensure Celery worker is running
   - Check Redis connection
   - Verify task imports in celery_app.py

4. **Database errors**
   - Check MongoDB connection string
   - Verify database permissions
   - Ensure indexes are created

## License

This project is licensed under the MIT License. 