from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.database import init_db
from datetime import datetime

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate):
    """Create a new user"""
    await init_db()
    
    # Check if username already exists
    existing_user = await User.find_one(User.username == user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email already exists
    existing_email = await User.find_one(User.email == user_data.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create user
    user = User(**user_data.dict())
    await user.insert()
    
    return user


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of users to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """Get list of users with optional filtering"""
    await init_db()
    
    # Build query
    query = {}
    if is_active is not None:
        query["is_active"] = is_active
    
    users = await User.find(query).skip(skip).limit(limit).to_list()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get a specific user by ID"""
    await init_db()
    
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_data: UserUpdate):
    """Update a user"""
    await init_db()
    
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check for username conflicts if username is being updated
    if user_data.username and user_data.username != user.username:
        existing_user = await User.find_one(User.username == user_data.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check for email conflicts if email is being updated
    if user_data.email and user_data.email != user.email:
        existing_email = await User.find_one(User.email == user_data.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    # Update only provided fields
    update_data = user_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    user.updated_at = datetime.utcnow()
    await user.save()
    
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Delete a user"""
    await init_db()
    
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await user.delete()
    
    return {"message": "User deleted successfully"}


@router.get("/stats/summary")
async def get_user_stats():
    """Get user statistics"""
    await init_db()
    
    total_users = await User.count()
    active_users = await User.find(User.is_active == True).count()
    inactive_users = await User.find(User.is_active == False).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users
    } 