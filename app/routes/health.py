from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

router = APIRouter()


@router.get("/", status_code=200)
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Advanced health check endpoint.
    Verifies application readiness by checking database connectivity.
    """
    try:
        # Simulate a database query to check connectivity
        result = await db.execute(text("SELECT 1"))
        if result.scalar_one() != 1:
            raise Exception("Unexpected database response")

        # If all checks pass, return healthy status
        return {"status": "healthy"}

    except Exception as e:
        # Log or handle errors and return unhealthy status
        raise HTTPException(status_code=503, detail={"status": "unhealthy", "reason": str(e)})
