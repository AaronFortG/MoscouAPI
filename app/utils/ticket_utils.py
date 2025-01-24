from typing import List, Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from app.schemas.ticket import TicketResponse


async def fetch_tickets(db: AsyncSession, filters: Dict, orders: List[Tuple[str, str]]) -> List[TicketResponse]:
    query = """
        SELECT
            tickets.*,
            users.name AS user_name,
            validators.name AS validator_name,
            events.name AS event_name
        FROM tickets
        JOIN users ON tickets.user_id = users.firebase_uid
        JOIN events ON tickets.event_id = events.event_id
        LEFT JOIN users AS validators ON tickets.validator_id = validators.firebase_uid
    """

    # Build WHERE clause dynamically
    conditions = []
    bind_params = {}

    if filters:
        for key, value in filters.items():
            if value is not None:  # Add only non-None filters
                conditions.append(f"tickets.{key} = :{key}")
                bind_params[key] = value

    # Add WHERE clause if there are conditions
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Add ORDER BY clause for multiple ordering fields
    if orders:
        valid_fields = {"purchased_at", "validated_date", "validated", "event_id", "user_id", "validator_id", "ticket_id"}
        order_clauses = []
        for field, direction in orders:
            if field in valid_fields:
                order_direction = "DESC" if direction == "desc" else "ASC"
                order_clauses.append(f"{field} {order_direction}")
        if order_clauses:
            query += " ORDER BY " + ", ".join(order_clauses)

    # Execute the query with bind parameters
    result = await db.execute(text(query), filters)
    tickets = result.mappings().all()

    return [TicketResponse(**ticket) for ticket in tickets]