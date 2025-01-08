from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketValidate
from app.database import get_db
from sqlalchemy.sql import func
from sqlalchemy.sql import text

router = APIRouter()

@router.post("/", response_model=dict)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    new_ticket = Ticket(
        user_id=ticket.user_id,
        event_id=ticket.event_id,
        qr_code=ticket.qr_code
    )
    db.add(new_ticket)
    try:
        await db.commit()
        return {"message": "Ticket created successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate", response_model=dict)
async def validate_ticket(ticket: TicketValidate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM tickets WHERE ticket_id = :ticket_id"), {"ticket_id": ticket.ticket_id})
    ticket_to_validate = result.scalar_one_or_none()

    if not ticket_to_validate:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket_to_validate.validator_id = ticket.validator_id
    ticket_to_validate.validated = True
    ticket_to_validate.validated_date = func.now()

    try:
        await db.commit()
        return {"message": "Ticket validated successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
