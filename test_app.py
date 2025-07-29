#!/usr/bin/env python3
"""
Test script for FastAPI Celery MongoDB Demo
"""
import asyncio
import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_create_user():
    """Test user creation"""
    print("Testing user creation...")
    user_data = {
        "username": "test_user",
        "email": "test@example.com",
        "full_name": "Test User"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/users/",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ User created: {user['id']}")
            return user['id']
        else:
            print(f"❌ User creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ User creation error: {e}")
        return None

def test_create_task():
    """Test task creation"""
    print("Testing task creation...")
    task_data = {
        "title": "Test Task",
        "description": "This is a test task for the demo",
        "priority": "medium"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/tasks/",
            json=task_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            task = response.json()
            print(f"✅ Task created: {task['id']}")
            return task['id']
        else:
            print(f"❌ Task creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Task creation error: {e}")
        return None

def test_start_task_processing(task_id):
    """Test task processing"""
    print(f"Testing task processing for task {task_id}...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/tasks/{task_id}/process?operation=data_processing"
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Task processing started: {result['task_id']}")
            return result['task_id']
        else:
            print(f"❌ Task processing failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Task processing error: {e}")
        return None

def test_get_task_status(task_id):
    """Test getting task status"""
    print(f"Testing task status for task {task_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/tasks/{task_id}/celery-status")
        
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Task status: {status['status']}")
            return status['status']
        else:
            print(f"❌ Task status check failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Task status check error: {e}")
        return None

def test_get_task_with_logs(task_id):
    """Test getting task with logs"""
    print(f"Testing task with logs for task {task_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/tasks/{task_id}/with-logs")
        
        if response.status_code == 200:
            task = response.json()
            print(f"✅ Task with logs retrieved: {len(task.get('logs', []))} logs")
            return True
        else:
            print(f"❌ Task with logs failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Task with logs error: {e}")
        return False

def test_get_statistics():
    """Test getting statistics"""
    print("Testing statistics...")
    
    try:
        # Task statistics
        response = requests.get(f"{BASE_URL}/tasks/stats/summary")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Task statistics: {stats['total_tasks']} total tasks")
        
        # User statistics
        response = requests.get(f"{BASE_URL}/users/stats/summary")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ User statistics: {stats['total_users']} total users")
        
        return True
    except Exception as e:
        print(f"❌ Statistics error: {e}")
        return False

def test_generate_report():
    """Test report generation"""
    print("Testing report generation...")
    
    try:
        response = requests.post(f"{BASE_URL}/tasks/generate-report?report_type=daily")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Report generation started: {result['celery_task_id']}")
            return True
        else:
            print(f"❌ Report generation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Report generation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting FastAPI Celery MongoDB Demo Tests")
    print("=" * 50)
    
    # Test health check
    if not test_health_check():
        print("❌ Application is not running. Please start the application first.")
        return
    
    print("\n" + "=" * 50)
    
    # Test user creation
    user_id = test_create_user()
    
    print("\n" + "=" * 50)
    
    # Test task creation
    task_id = test_create_task()
    
    if task_id:
        print("\n" + "=" * 50)
        
        # Test task processing
        celery_task_id = test_start_task_processing(task_id)
        
        if celery_task_id:
            print("\n" + "=" * 50)
            
            # Wait a bit for processing to start
            print("⏳ Waiting for task processing to start...")
            time.sleep(2)
            
            # Test task status
            status = test_get_task_status(task_id)
            
            print("\n" + "=" * 50)
            
            # Test task with logs
            test_get_task_with_logs(task_id)
    
    print("\n" + "=" * 50)
    
    # Test statistics
    test_get_statistics()
    
    print("\n" + "=" * 50)
    
    # Test report generation
    test_generate_report()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\n📚 API Documentation available at:")
    print(f"   - Swagger UI: {BASE_URL}/docs")
    print(f"   - ReDoc: {BASE_URL}/redoc")
    print(f"   - Flower (Celery monitoring): http://localhost:5555")

if __name__ == "__main__":
    main() 