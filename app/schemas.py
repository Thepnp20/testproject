from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    priority: Optional[TaskPriority] = Field(None, description="Task priority")


class TaskResponse(TaskBase):
    id: str = Field(..., description="Task ID")
    status: TaskStatus = Field(..., description="Task status")
    celery_task_id: Optional[str] = Field(None, description="Celery task ID")
    result: Optional[str] = Field(None, description="Task result")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str = Field(..., description="Unique username")
    email: str = Field(..., description="User email")
    full_name: str = Field(..., description="User full name")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="Unique username")
    email: Optional[str] = Field(None, description="User email")
    full_name: Optional[str] = Field(None, description="User full name")
    is_active: Optional[bool] = Field(None, description="User active status")


class UserResponse(UserBase):
    id: str = Field(..., description="User ID")
    is_active: bool = Field(..., description="User active status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True


class TaskLogResponse(BaseModel):
    id: str = Field(..., description="Log ID")
    task_id: str = Field(..., description="Reference to task ID")
    message: str = Field(..., description="Log message")
    level: str = Field(..., description="Log level")
    timestamp: datetime = Field(..., description="Log timestamp")
    
    class Config:
        from_attributes = True


class TaskWithLogsResponse(TaskResponse):
    logs: List[TaskLogResponse] = Field(default=[], description="Task logs")


class CeleryTaskResponse(BaseModel):
    task_id: str = Field(..., description="Celery task ID")
    status: str = Field(..., description="Task status")
    result: Optional[str] = Field(None, description="Task result") 