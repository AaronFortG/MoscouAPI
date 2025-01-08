from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import Event
from app.schemas.event import EventCreate
from app.database import get_db
from sqlalchemy.sql import text

router = APIRouter()

@router.get("/")
async def get_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM events"))
    return result.mappings().all()

@router.post("/")
async def create_event(event: EventCreate, db: AsyncSession = Depends(get_db)):
    new_event = Event(
        name=event.name,
        price=event.price,
        image_url=event.image_url,
        event_date=event.event_date
    )
    db.add(new_event)
    try:
        await db.commit()
        return {"message": "Event created successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
