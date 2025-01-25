from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, null
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import TicketModel
from app.routes.event import event_exists
from app.schemas.ticket import TicketCreate, TicketValidate, TicketResponse
from app.database import get_db
from sqlalchemy.sql import func
from app.routes.user import user_exists
from app.utils.ticket_utils import fetch_tickets_scheme

router = APIRouter()


@router.get("/", response_model=List[TicketResponse])
async def get_tickets(
    db: AsyncSession = Depends(get_db),
    event_id: Optional[int] = Query(default=None),  # Filter by event ID
    user_id: Optional[str] = Query(default=None),  # Filter by user ID
    validator_id: Optional[str] = Query(default=None),  # Filter by validator ID
    validated: Optional[bool] = Query(default=None),  # Filter by validated status
    order_by: Optional[List[str]] = Query(default=None),  # List of fields to order by
    order_directions: Optional[List[str]] = Query(default=None)  # Corresponding directions: asc or desc
):
    # Build filters dictionary
    filters = {
        "event_id": event_id,
        "user_id": user_id,
        "validator_id": validator_id,
        "validated": validated,
    }
    orders = list(zip(order_by or [], (direction.lower() for direction in (order_directions or []))))
    return await fetch_tickets_scheme(db, filters, orders)


@router.post("/", response_model=dict)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    # Check if the user exists
    if not await user_exists(db, ticket.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the event exists
    if not await event_exists(db, ticket.event_id):
        raise HTTPException(status_code=404, detail="Event not found")

    new_ticket = TicketModel(
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
        raise HTTPException(status_code=500, detail="Failed to create ticket")


@router.post("/validate/{ticket_id}", response_model=dict)
async def validate_ticket(ticket_id: int, ticket: TicketValidate, db: AsyncSession = Depends(get_db)):
    # Check if the ticket exists
    ticket_to_validate = await ticket_exists(db, ticket_id)
    if not ticket_to_validate:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Check if the ticket is already validated.
    if ticket_to_validate.validated:
        raise HTTPException(status_code=409, detail="Ticket is already validated")

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
        raise HTTPException(status_code=500, detail="Failed to validate ticket")


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
        raise HTTPException(status_code=409, detail="Cannot invalidate a ticket that is not validated")

    # Set the ticket as not validated
    ticket_to_delete.validator_id = null
    ticket_to_delete.validated = False
    ticket_to_delete.validated_date = null

    try:
        await db.commit()
        return {"message": f"Ticket with ID {ticket_id} has been unvalidated successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete the ticket: {str(e)}")


# Query the ticket on the database
async def ticket_exists(db: AsyncSession, ticket_id: int) -> TicketModel | None:
    result = await db.execute(select(TicketModel).where(TicketModel.ticket_id == ticket_id))
    return result.scalar_one_or_none()
