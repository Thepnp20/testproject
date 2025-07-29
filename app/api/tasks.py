from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.models import Task, TaskLog, TaskStatus, TaskPriority
from app.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskWithLogsResponse, CeleryTaskResponse
from app.tasks import process_task, cleanup_old_tasks, generate_report
from app.database import init_db
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
async def create_task(task_data: TaskCreate):
    """Create a new task"""
    await init_db()
    
    # Create task in database
    task = Task(**task_data.dict())
    await task.insert()
    
    return task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of tasks to return"),
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by task priority")
):
    """Get list of tasks with optional filtering"""
    await init_db()
    
    # Build query
    query = {}
    if status:
        query["status"] = status
    if priority:
        query["priority"] = priority
    
    tasks = await Task.find(query).skip(skip).limit(limit).to_list()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get a specific task by ID"""
    await init_db()
    
    task = await Task.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.get("/{task_id}/with-logs", response_model=TaskWithLogsResponse)
async def get_task_with_logs(task_id: str):
    """Get a task with its execution logs"""
    await init_db()
    
    task = await Task.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Get task logs
    logs = await TaskLog.find(TaskLog.task_id == task_id).to_list()
    
    # Create response with logs
    task_dict = task.dict()
    task_dict["logs"] = logs
    
    return task_dict


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_data: TaskUpdate):
    """Update a task"""
    await init_db()
    
    task = await Task.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update only provided fields
    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    task.updated_at = datetime.utcnow()
    await task.save()
    
    return task


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Delete a task and its logs"""
    await init_db()
    
    task = await Task.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Delete associated logs
    await TaskLog.find(TaskLog.task_id == task_id).delete()
    
    # Delete task
    await task.delete()
    
    return {"message": "Task deleted successfully"}


@router.post("/{task_id}/process", response_model=CeleryTaskResponse)
async def start_task_processing(
    task_id: str,
    operation: str = Query("default", description="Type of operation to perform")
):
    """Start processing a task with Celery"""
    await init_db()
    
    task = await Task.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status != TaskStatus.PENDING:
        raise HTTPException(status_code=400, detail="Task is not in pending status")
    
    # Start Celery task
    celery_task = process_task.delay(task_id, operation)
    
    # Update task with Celery task ID
    task.celery_task_id = celery_task.id
    task.status = TaskStatus.PROCESSING
    task.updated_at = datetime.utcnow()
    await task.save()
    
    return {
        "task_id": celery_task.id,
        "status": celery_task.status,
        "result": None
    }


@router.get("/{task_id}/celery-status", response_model=CeleryTaskResponse)
async def get_celery_task_status(task_id: str):
    """Get the status of a Celery task"""
    await init_db()
    
    task = await Task.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if not task.celery_task_id:
        raise HTTPException(status_code=400, detail="Task has no associated Celery task")
    
    # Get Celery task status
    from app.celery_app import celery_app
    celery_task = celery_app.AsyncResult(task.celery_task_id)
    
    return {
        "task_id": celery_task.id,
        "status": celery_task.status,
        "result": celery_task.result if celery_task.ready() else None
    }


@router.post("/cleanup")
async def cleanup_tasks(days_old: int = Query(30, ge=1, description="Delete tasks older than this many days")):
    """Clean up old completed tasks"""
    celery_task = cleanup_old_tasks.delay(days_old)
    
    return {
        "message": "Cleanup task started",
        "celery_task_id": celery_task.id
    }


@router.post("/generate-report")
async def start_report_generation(
    report_type: str = Query("daily", description="Type of report to generate")
):
    """Generate a report"""
    celery_task = generate_report.delay(report_type)
    
    return {
        "message": f"{report_type.capitalize()} report generation started",
        "celery_task_id": celery_task.id
    }


@router.get("/stats/summary")
async def get_task_stats():
    """Get task statistics"""
    await init_db()
    
    # Get counts by status
    pending_count = await Task.find(Task.status == TaskStatus.PENDING).count()
    processing_count = await Task.find(Task.status == TaskStatus.PROCESSING).count()
    completed_count = await Task.find(Task.status == TaskStatus.COMPLETED).count()
    failed_count = await Task.find(Task.status == TaskStatus.FAILED).count()
    
    # Get counts by priority
    low_count = await Task.find(Task.priority == TaskPriority.LOW).count()
    medium_count = await Task.find(Task.priority == TaskPriority.MEDIUM).count()
    high_count = await Task.find(Task.priority == TaskPriority.HIGH).count()
    
    return {
        "total_tasks": pending_count + processing_count + completed_count + failed_count,
        "by_status": {
            "pending": pending_count,
            "processing": processing_count,
            "completed": completed_count,
            "failed": failed_count
        },
        "by_priority": {
            "low": low_count,
            "medium": medium_count,
            "high": high_count
        }
    } 