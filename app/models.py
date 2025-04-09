from pydantic import BaseModel, Field
from typing import List
from datetime import date, time
import uuid

# --- Item model ---
class Item(BaseModel):
    shortDescription: str = Field(
        ...,
        description="The Short Product Description for the item.",
        pattern=r"^[\w\s\-]+$",
        example="Mountain Dew 12PK"
    )
    price: str = Field(
        ...,
        description="The total price paid for this item.",
        pattern=r"^\d+\.\d{2}$",
        example="6.49"
    )

# --- Receipt model ---
class Receipt(BaseModel):
    retailer: str = Field(
        ...,
        description="The name of the retailer or store the receipt is from.",
        pattern=r"^[\w\s\-&]+$",
        example="M&M Corner Market"
    )
    purchaseDate: date = Field(
        ...,
        description="The date of the purchase printed on the receipt.",
        example="2022-01-01"
    )
    purchaseTime: time = Field(
        ...,
        description="The time of the purchase printed on the receipt (24-hour time).",
        example="13:01"
    )
    items: List[Item] = Field(
        ...,
        min_items=1,
        description="List of items purchased"
    )
    total: str = Field(
        ...,
        description="The total amount paid on the receipt.",
        pattern=r"^\d+\.\d{2}$",
        example="6.49"
    )

# --- Response models ---
class ReceiptID(BaseModel):
    id: str = Field(..., example="adb6b560-0eef-42bc-9d16-df48f30e89b2")

class Points(BaseModel):
    points: int = Field(..., example=100)

# --- ID Generator ---
def generate_receipt_id() -> str:
    """Generate a unique ID for a receipt."""
    return str(uuid.uuid4())
