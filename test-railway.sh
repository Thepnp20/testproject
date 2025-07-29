#!/bin/bash

# Railway Deployment Test Script

echo "🧪 Testing Railway Deployment"
echo "============================="

# Check if APP_URL is provided
if [ -z "$APP_URL" ]; then
    echo "❌ APP_URL environment variable is not set."
    echo "Please set your Railway app URL:"
    echo "export APP_URL=https://your-app-name.railway.app"
    echo ""
    echo "Example:"
    echo "export APP_URL=https://fastapi-celery-demo.railway.app"
    exit 1
fi

echo "✅ Testing app at: $APP_URL"
echo ""

# Test health check
echo "🔍 Testing health check..."
if curl -f -s "$APP_URL/health" > /dev/null; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

# Test API documentation
echo "🔍 Testing API documentation..."
if curl -f -s "$APP_URL/docs" > /dev/null; then
    echo "✅ API documentation accessible"
else
    echo "❌ API documentation not accessible"
fi

# Test task creation
echo "🔍 Testing task creation..."
TASK_RESPONSE=$(curl -s -X POST "$APP_URL/tasks/" \
    -H "Content-Type: application/json" \
    -d '{
        "title": "Railway Test Task",
        "description": "Testing Railway deployment functionality",
        "priority": "medium"
    }')

if echo "$TASK_RESPONSE" | grep -q "id"; then
    echo "✅ Task creation successful"
    TASK_ID=$(echo "$TASK_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    echo "   Task ID: $TASK_ID"
else
    echo "❌ Task creation failed"
    echo "   Response: $TASK_RESPONSE"
fi

# Test task processing
if [ ! -z "$TASK_ID" ]; then
    echo "🔍 Testing task processing..."
    PROCESS_RESPONSE=$(curl -s -X POST "$APP_URL/tasks/$TASK_ID/process?operation=data_processing")
    
    if echo "$PROCESS_RESPONSE" | grep -q "task_id"; then
        echo "✅ Task processing started"
        CELERY_TASK_ID=$(echo "$PROCESS_RESPONSE" | grep -o '"task_id":"[^"]*"' | cut -d'"' -f4)
        echo "   Celery Task ID: $CELERY_TASK_ID"
    else
        echo "❌ Task processing failed"
        echo "   Response: $PROCESS_RESPONSE"
    fi
fi

# Test statistics
echo "🔍 Testing statistics endpoints..."
if curl -f -s "$APP_URL/tasks/stats/summary" > /dev/null; then
    echo "✅ Task statistics accessible"
else
    echo "❌ Task statistics not accessible"
fi

if curl -f -s "$APP_URL/users/stats/summary" > /dev/null; then
    echo "✅ User statistics accessible"
else
    echo "❌ User statistics not accessible"
fi

# Test user creation
echo "🔍 Testing user creation..."
USER_RESPONSE=$(curl -s -X POST "$APP_URL/users/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "railway_test_user",
        "email": "test@railway.com",
        "full_name": "Railway Test User"
    }')

if echo "$USER_RESPONSE" | grep -q "id"; then
    echo "✅ User creation successful"
    USER_ID=$(echo "$USER_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    echo "   User ID: $USER_ID"
else
    echo "❌ User creation failed"
    echo "   Response: $USER_RESPONSE"
fi

echo ""
echo "🎉 Railway deployment test completed!"
echo ""
echo "📚 Available endpoints:"
echo "   - Health: $APP_URL/health"
echo "   - API Docs: $APP_URL/docs"
echo "   - Tasks: $APP_URL/tasks/"
echo "   - Users: $APP_URL/users/"
echo ""
echo "🔧 To monitor your deployment:"
echo "   - Check Railway dashboard for logs"
echo "   - Monitor service health in Railway"
echo "   - View deployment status and metrics" 