#!/bin/bash

# One-Click Railway Instant Deployment Script

echo "🚀 FastAPI Celery MongoDB Demo - Instant Deployment"
echo "===================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check prerequisites
print_status "Checking prerequisites..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    print_warning "Railway CLI is not installed. Installing now..."
    npm install -g @railway/cli
fi

# Check if user is logged in to Railway
if ! railway whoami &> /dev/null; then
    print_warning "Not logged in to Railway. Please login first:"
    echo "railway login"
    exit 1
fi

print_success "Prerequisites check completed"

# Get repository information
print_status "Getting repository information..."

# Get current git remote URL
REPO_URL=$(git remote get-url origin 2>/dev/null)
if [ -z "$REPO_URL" ]; then
    print_error "No git remote found. Please add a remote origin first:"
    echo "git remote add origin https://github.com/your-username/your-repo-name.git"
    exit 1
fi

# Extract repository name from URL
REPO_NAME=$(basename -s .git "$REPO_URL")
print_success "Repository: $REPO_NAME"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_error "Not in a git repository. Please initialize git first:"
    echo "git init"
    echo "git add ."
    echo "git commit -m 'Initial commit'"
    exit 1
fi

# Check if we have uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    print_warning "You have uncommitted changes. Committing them now..."
    git add .
    git commit -m "Update for Railway deployment"
fi

# Push to remote if needed
print_status "Pushing to remote repository..."
git push origin main

print_success "Repository is ready for deployment"

# Initialize Railway project if not already done
if [ ! -f ".railway" ]; then
    print_status "Initializing Railway project..."
    railway init
fi

# Create deployment configuration
print_status "Creating deployment configuration..."

# Update the railway-deploy.json with actual repository info
sed -i "s/your-username\/your-repo-name/$REPO_NAME/g" railway-deploy.json

print_success "Deployment configuration created"

# Deploy using Railway CLI
print_status "Starting deployment..."

# Deploy the application
print_status "Deploying FastAPI application..."
if railway up; then
    print_success "Deployment started successfully!"
    
    # Get the deployment URL
    print_status "Getting deployment URL..."
    DEPLOYMENT_URL=$(railway status --json | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$DEPLOYMENT_URL" ]; then
        print_success "Your application is deployed at: $DEPLOYMENT_URL"
        
        # Test the deployment
        print_status "Testing deployment..."
        sleep 30  # Wait for deployment to complete
        
        if curl -f -s "$DEPLOYMENT_URL/health" > /dev/null; then
            print_success "Deployment test successful!"
            
            echo ""
            echo "🎉 Deployment completed successfully!"
            echo ""
            echo "📚 Your application is now live:"
            echo "   - Main URL: $DEPLOYMENT_URL"
            echo "   - Health Check: $DEPLOYMENT_URL/health"
            echo "   - API Documentation: $DEPLOYMENT_URL/docs"
            echo "   - Tasks API: $DEPLOYMENT_URL/tasks"
            echo "   - Users API: $DEPLOYMENT_URL/users"
            echo ""
            echo "🔧 Management:"
            echo "   - Railway Dashboard: https://railway.app"
            echo "   - View Logs: railway logs"
            echo "   - Check Status: railway status"
            echo ""
            echo "🧪 Test your deployment:"
            echo "   export APP_URL=$DEPLOYMENT_URL"
            echo "   ./test-railway.sh"
            
        else
            print_warning "Deployment test failed. Check Railway dashboard for logs."
        fi
    else
        print_warning "Could not get deployment URL. Check Railway dashboard."
    fi
else
    print_error "Deployment failed. Check Railway dashboard for details."
    exit 1
fi

echo ""
print_status "Deployment process completed!"
print_status "Visit https://railway.app to monitor your deployment." 