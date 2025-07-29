#!/usr/bin/env python3
"""
Celery Worker for FastAPI Celery MongoDB Demo
"""
from app.celery_app import celery_app

if __name__ == "__main__":
    celery_app.start() 