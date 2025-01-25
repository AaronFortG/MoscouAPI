from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, literal
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import EventModel
from app.schemas.event import EventSchema
from app.database import get_db
from sqlalchemy.sql import text

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import qrcode
import io

router = APIRouter()


# Helper function to generate QR codes
def create_qr_image(data: str, box_size: int, border: int, fill_color: str, back_color: str):
    """
    Helper function to generate a QR code image.
    """
    if not data:
        raise HTTPException(status_code=400, detail="Data is required to generate a QR code")

    # Create a QR code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Generate the QR code image
    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    # Save the image to an in-memory buffer
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer


@router.post("/")
async def generate_qr(data: str):
    """
    Generate a QR code for the given data.
    """
    buffer = create_qr_image(data, box_size=10, border=4, fill_color="black", back_color="white")
    return StreamingResponse(buffer, media_type="image/png")

@router.post("/advanced/")
async def generate_qr_advanced(data: str, box_size: int = 10, border: int = 4, fill_color: str = "black", back_color: str = "white"):
    """
    Generate a QR code for the given data with customizable options.
    """
    buffer = create_qr_image(data, box_size=box_size, border=border, fill_color=fill_color, back_color=back_color)
    return StreamingResponse(buffer, media_type="image/png")