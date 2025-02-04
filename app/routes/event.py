from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, literal
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import EventModel
from app.schemas.event import EventSchema
from app.database import get_db
from sqlalchemy.sql import text

from app.schemas.ticket import TicketResponse
from app.utils.ticket_utils import fetch_tickets_scheme

router = APIRouter()


@router.get("/", response_model=List[EventSchema])
async def get_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM events"))
    return result.mappings().all()


@router.post("/")
async def create_event(event: EventSchema, db: AsyncSession = Depends(get_db)):
    new_event = EventModel(
        name=event.name,
        price=event.price,
        description=event.description,
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


@router.get("/{event_id}/tickets/", response_model=List[TicketResponse])
async def get_event_tickets(event_id: int, db: AsyncSession = Depends(get_db)):
    # Build the filters dictionary
    filters = {
        "event_id": event_id,
    }
    return await fetch_tickets_scheme(db, filters, [])

async def event_exists(db: AsyncSession, event_id: int) -> EventModel | None:
    result = await db.execute(select(EventModel).where(EventModel.event_id == event_id))
    return result.scalar_one_or_none()
