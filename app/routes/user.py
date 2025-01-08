from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=dict)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(firebase_uid=user.firebase_uid, name=user.name, email=user.email)
    db.add(new_user)
    try:
        await db.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
