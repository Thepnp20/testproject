#!/bin/bash

# Celery Worker Status Check Script

echo "🔍 Checking Celery Worker Status"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Railway CLI is available
if command -v railway &> /dev/null; then
    print_status "Railway CLI found. Checking services..."
    
    # Check if we're in a Railway project
    if [ -f ".railway" ]; then
        print_success "Railway project detected"
        
        # Get service status
        print_status "Getting service status..."
        railway status
        
        # Check logs for Celery worker
        print_status "Checking Celery worker logs..."
        railway logs --service celery-worker --tail 20
        
    else
        print_warning "Not in a Railway project. Please run this from your project directory."
    fi
else
    print_warning "Railway CLI not found. Install with: npm install -g @railway/cli"
fi

echo ""
print_status "Manual Celery Worker Checks:"
echo ""

# Check if we can connect to Redis
print_status "Testing Redis connection..."
if python3 -c "
import redis
try:
    r = redis.Redis(host='localhost', port=6379)
    r.ping()
    print('✅ Redis connection successful')
except Exception as e:
    print(f'❌ Redis connection failed: {e}')
" 2>/dev/null; then
    print_success "Redis connection test completed"
else
    print_warning "Redis connection test failed (expected if not running locally)"
fi

# Check Celery worker status
print_status "Testing Celery worker..."
if python3 -c "
from app.celery_app import celery_app
try:
    i = celery_app.control.inspect()
    stats = i.stats()
    if stats:
        print('✅ Celery worker is running')
        for worker, info in stats.items():
            print(f'   Worker: {worker}')
            print(f'   Pool: {info.get(\"pool\", {}).get(\"implementation\", \"unknown\")}')
    else:
        print('❌ No Celery workers found')
except Exception as e:
    print(f'❌ Celery worker check failed: {e}')
" 2>/dev/null; then
    print_success "Celery worker check completed"
else
    print_warning "Celery worker check failed (expected if not running locally)"
fi

echo ""
print_status "Railway Dashboard Checks:"
echo "1. Go to https://railway.app"
echo "2. Check your project"
echo "3. Look for 'celery-worker' service"
echo "4. Check logs for any errors"
echo "5. Verify the service is running"
echo ""
print_status "Celery Worker Monitoring:"
echo "- Worker logs: railway logs --service celery-worker"
echo "- Service status: railway status"
echo "- Restart worker: railway restart --service celery-worker" 