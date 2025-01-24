from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket
from app.routes.event import event_exists
from app.schemas.ticket import TicketCreate, TicketValidate, TicketResponse
from app.database import get_db
from sqlalchemy.sql import func
from sqlalchemy.sql import text
from sqlalchemy.future import select
from app.routes.user import user_exists

router = APIRouter()


@router.get("/", response_model=List[TicketResponse])
async def get_tickets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("""
            SELECT 
                tickets.*, 
                users.name AS user_name, 
                validators.name AS validator_name
            FROM tickets
            JOIN users ON tickets.user_id = users.firebase_uid
            LEFT JOIN users AS validators ON tickets.validator_id = validators.firebase_uid
        """))
    tickets = result.mappings().all()

    return [TicketResponse(**ticket) for ticket in tickets]


@router.post("/", response_model=dict)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    # Check if the user exists
    if not await user_exists(db, ticket.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the event exists
    if not await event_exists(db, ticket.event_id):
        raise HTTPException(status_code=404, detail="Event not found")

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


@router.post("/validate/{ticket_id}", response_model=dict)
async def validate_ticket(ticket_id: int, ticket: TicketValidate, db: AsyncSession = Depends(get_db)):
    # Check if the ticket exists
    ticket_to_validate = await ticket_exists(db, ticket_id)
    if not ticket_to_validate:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Check if the ticket is already validated.
    if ticket_to_validate.validated:
        raise HTTPException(status_code=400, detail="Ticket is already validated")

    # Check if validator exists
    if not await user_exists(db, ticket.validator_id):
        raise HTTPException(status_code=404, detail="Validator not found")

    ticket_to_validate.validator_id = ticket.validator_id
    ticket_to_validate.validated = True
    ticket_to_validate.validated_date = func.now()

    try:
        await db.commit()
        return {"message": "Ticket validated successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/validate/{ticket_id}", response_model=dict)
async def delete_validated_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    """
    Deletes a validated ticket by ticket_id if it is validated.
    """
    # Check if the ticket exists
    ticket_to_delete = await ticket_exists(db, ticket_id)
    if not ticket_to_delete:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Check if the ticket is validated
    if not ticket_to_delete.validated:
        raise HTTPException(status_code=400, detail="Cannot delete a ticket that is not validated")

    # Delete the ticket
    await db.delete(ticket_to_delete)
    try:
        await db.commit()
        return {"message": f"Validated ticket with ID {ticket_id} has been deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete the ticket: {str(e)}")


async def ticket_exists(db: AsyncSession, ticket_id: int) -> Ticket:
    result = await db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id))
    return result.scalar_one_or_none()
