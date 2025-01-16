from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserResponse
from app.database import get_db
from sqlalchemy import text
from sqlalchemy.future import select

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM users"))
    return result.mappings().all()


@router.post("/", response_model=List[UserResponse])
async def create_user(user: UserResponse, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    if await user_exists(db, user.firebase_uid):
        raise HTTPException(status_code=400, detail="User already exists.")

    # Create new user
    new_user = User(firebase_uid=user.firebase_uid, name=user.name, email=user.email)
    db.add(new_user)
    try:
        await db.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


async def user_exists(db: AsyncSession, firebase_uid: str) -> User:
    existing_user = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    return existing_user.scalar_one_or_none()
