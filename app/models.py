from datetime import datetime
from typing import Optional, List
from beanie import Document, Indexed
from pydantic import Field
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Document):
    """Task model for storing background task information"""
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority")
    celery_task_id: Optional[str] = Field(None, description="Celery task ID")
    result: Optional[str] = Field(None, description="Task result")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    
    class Settings:
        name = "tasks"
        indexes = [
            "status",
            "priority",
            "created_at",
            ("status", "priority"),
        ]


class User(Document):
    """User model for storing user information"""
    username: Indexed(str, unique=True) = Field(..., description="Unique username")
    email: Indexed(str, unique=True) = Field(..., description="User email")
    full_name: str = Field(..., description="User full name")
    is_active: bool = Field(default=True, description="User active status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Settings:
        name = "users"
        indexes = [
            "username",
            "email",
            "is_active",
        ]


class TaskLog(Document):
    """Task log model for storing task execution logs"""
    task_id: str = Field(..., description="Reference to task ID")
    message: str = Field(..., description="Log message")
    level: str = Field(default="info", description="Log level")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Log timestamp")
    
    class Settings:
        name = "task_logs"
        indexes = [
            "task_id",
            "timestamp",
            "level",
        ] 