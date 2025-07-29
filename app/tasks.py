import time
import random
import logging
from datetime import datetime
from typing import Optional
from celery import current_task
from app.celery_app import celery_app
from app.models import Task, TaskLog, TaskStatus
from app.database import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def process_task(self, task_id: str, operation: str = "default"):
    """
    Process a task with various operations
    """
    import asyncio
    
    async def _process_task_async():
        try:
            # Initialize database connection
            await init_db()
            
            # Update task status to processing
            task = await Task.get(task_id)
            if not task:
                raise ValueError(f"Task {task_id} not found")
            
            task.status = TaskStatus.PROCESSING
            task.updated_at = datetime.utcnow()
            await task.save()
            
            # Log task start
            await TaskLog(
                task_id=task_id,
                message=f"Started processing task with operation: {operation}",
                level="info"
            ).insert()
            
            # Simulate different types of processing based on operation
            if operation == "data_processing":
                result = await _process_data_operation(task_id)
            elif operation == "file_processing":
                result = await _process_file_operation(task_id)
            elif operation == "email_sending":
                result = await _process_email_operation(task_id)
            else:
                result = await _process_default_operation(task_id)
            
            # Update task as completed
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.completed_at = datetime.utcnow()
            task.updated_at = datetime.utcnow()
            await task.save()
            
            # Log completion
            await TaskLog(
                task_id=task_id,
                message=f"Task completed successfully with result: {result}",
                level="info"
            ).insert()
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing task {task_id}: {str(e)}")
            
            # Update task as failed
            task = await Task.get(task_id)
            if task:
                task.status = TaskStatus.FAILED
                task.error_message = str(e)
                task.updated_at = datetime.utcnow()
                await task.save()
            
            # Log error
            await TaskLog(
                task_id=task_id,
                message=f"Task failed with error: {str(e)}",
                level="error"
            ).insert()
            
            raise
    
    return asyncio.run(_process_task_async())


async def _process_data_operation(task_id: str) -> str:
    """Simulate data processing operation"""
    await TaskLog(
        task_id=task_id,
        message="Starting data processing operation",
        level="info"
    ).insert()
    
    # Simulate processing time
    time.sleep(random.uniform(2, 5))
    
    # Simulate data transformation
    processed_data = {
        "records_processed": random.randint(100, 1000),
        "data_size_mb": round(random.uniform(1.5, 10.2), 2),
        "processing_time_seconds": round(random.uniform(2, 8), 2)
    }
    
    await TaskLog(
        task_id=task_id,
        message=f"Data processing completed: {processed_data}",
        level="info"
    ).insert()
    
    return f"Data processing completed successfully. Processed {processed_data['records_processed']} records."


async def _process_file_operation(task_id: str) -> str:
    """Simulate file processing operation"""
    await TaskLog(
        task_id=task_id,
        message="Starting file processing operation",
        level="info"
    ).insert()
    
    # Simulate file operations
    time.sleep(random.uniform(3, 7))
    
    file_operations = [
        "File validation completed",
        "File format conversion in progress",
        "Metadata extraction completed",
        "File compression applied",
        "Quality checks passed"
    ]
    
    for operation in file_operations:
        await TaskLog(
            task_id=task_id,
            message=operation,
            level="info"
        ).insert()
        time.sleep(random.uniform(0.5, 1.5))
    
    return "File processing completed successfully. All operations passed quality checks."


async def _process_email_operation(task_id: str) -> str:
    """Simulate email sending operation"""
    await TaskLog(
        task_id=task_id,
        message="Starting email sending operation",
        level="info"
    ).insert()
    
    # Simulate email processing
    time.sleep(random.uniform(1, 3))
    
    email_data = {
        "recipients": random.randint(10, 100),
        "templates_used": random.randint(1, 5),
        "delivery_rate": round(random.uniform(95, 99.9), 1)
    }
    
    await TaskLog(
        task_id=task_id,
        message=f"Email campaign completed: {email_data}",
        level="info"
    ).insert()
    
    return f"Email campaign completed. Sent to {email_data['recipients']} recipients with {email_data['delivery_rate']}% delivery rate."


async def _process_default_operation(task_id: str) -> str:
    """Default processing operation"""
    await TaskLog(
        task_id=task_id,
        message="Starting default processing operation",
        level="info"
    ).insert()
    
    # Simulate generic processing
    time.sleep(random.uniform(1, 4))
    
    await TaskLog(
        task_id=task_id,
        message="Default processing completed",
        level="info"
    ).insert()
    
    return "Default processing completed successfully."


@celery_app.task(bind=True)
def cleanup_old_tasks(self, days_old: int = 30):
    """
    Clean up old completed tasks
    """
    import asyncio
    
    async def _cleanup_old_tasks_async():
        try:
            await init_db()
            
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            # Find old completed tasks
            old_tasks = await Task.find(
                Task.status == TaskStatus.COMPLETED,
                Task.completed_at < cutoff_date
            ).to_list()
            
            deleted_count = 0
            for task in old_tasks:
                # Delete associated logs
                await TaskLog.find(TaskLog.task_id == str(task.id)).delete()
                # Delete task
                await task.delete()
                deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} old tasks")
            return f"Cleaned up {deleted_count} old tasks"
            
        except Exception as e:
            logger.error(f"Error cleaning up old tasks: {str(e)}")
            raise
    
    return asyncio.run(_cleanup_old_tasks_async())


@celery_app.task(bind=True)
def generate_report(self, report_type: str = "daily"):
    """
    Generate various types of reports
    """
    import asyncio
    
    async def _generate_report_async():
        try:
            await init_db()
            
            await TaskLog(
                task_id="report_generation",
                message=f"Starting {report_type} report generation",
                level="info"
            ).insert()
            
            # Simulate report generation
            time.sleep(random.uniform(5, 15))
            
            if report_type == "daily":
                report_data = {
                    "total_tasks": random.randint(50, 200),
                    "completed_tasks": random.randint(40, 180),
                    "failed_tasks": random.randint(1, 10),
                    "avg_processing_time": round(random.uniform(2, 8), 2)
                }
            elif report_type == "weekly":
                report_data = {
                    "total_tasks": random.randint(300, 1000),
                    "completed_tasks": random.randint(280, 950),
                    "failed_tasks": random.randint(5, 30),
                    "avg_processing_time": round(random.uniform(2, 8), 2),
                    "peak_hours": ["09:00-11:00", "14:00-16:00"]
                }
            else:
                report_data = {
                    "total_tasks": random.randint(1000, 5000),
                    "completed_tasks": random.randint(950, 4800),
                    "failed_tasks": random.randint(20, 100),
                    "avg_processing_time": round(random.uniform(2, 8), 2)
                }
            
            await TaskLog(
                task_id="report_generation",
                message=f"{report_type.capitalize()} report generated: {report_data}",
                level="info"
            ).insert()
            
            return f"{report_type.capitalize()} report generated successfully with {report_data['total_tasks']} total tasks"
            
        except Exception as e:
            logger.error(f"Error generating {report_type} report: {str(e)}")
            raise
    
    return asyncio.run(_generate_report_async()) 