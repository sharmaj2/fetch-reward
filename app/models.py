# from pydantic import BaseModel, Field, field_validator
# from typing import List, Optional
# import re
# from datetime import date, time
# import uuid

# class Item(BaseModel):
#     shortDescription: str = Field(..., pattern=r"^[\w\s\-]+$", example="Mountain Dew 12PK")
#     price: str = Field(..., pattern=r"^\d+\.\d{2}$", example="6.49")
    
#     @field_validator('shortDescription')
#     @classmethod
#     def validate_short_description(cls, v):
#         if not re.match(r"^[\w\s\-]+$", v):
#             raise ValueError("Short description must contain only alphanumeric characters, spaces, and hyphens")
#         return v
    
#     @field_validator('price')
#     @classmethod
#     def validate_price(cls, v):
#         if not re.match(r"^\d+\.\d{2}$", v):
#             raise ValueError("Price must be in the format X.XX")
#         return v

# class Receipt(BaseModel):
#     retailer: str = Field(..., pattern=r"^[\w\s\-&]+$", example="M&M Corner Market")
#     purchaseDate: str = Field(..., example="2022-01-01")
#     purchaseTime: str = Field(..., example="13:01")
#     items: List[Item] = Field(..., min_items=1)
#     total: str = Field(..., pattern=r"^\d+\.\d{2}$", example="6.49")
    
#     @field_validator('retailer')
#     @classmethod
#     def validate_retailer(cls, v):
#         if not re.match(r"^[\w\s\-&]+$", v):
#             raise ValueError("Retailer must contain only alphanumeric characters, spaces, hyphens, and ampersands")
#         return v
    
#     @field_validator('purchaseDate')
#     @classmethod
#     def validate_purchase_date(cls, v):
#         try:
#             year, month, day = map(int, v.split('-'))
#             date(year, month, day)
#         except (ValueError, TypeError):
#             raise ValueError("Purchase date must be in the format YYYY-MM-DD")
#         return v
    
#     @field_validator('purchaseTime')
#     @classmethod
#     def validate_purchase_time(cls, v):
#         try:
#             hour, minute = map(int, v.split(':'))
#             time(hour, minute)
#         except (ValueError, TypeError):
#             raise ValueError("Purchase time must be in the format HH:MM (24-hour)")
#         return v
    
#     @field_validator('total')
#     @classmethod
#     def validate_total(cls, v):
#         if not re.match(r"^\d+\.\d{2}$", v):
#             raise ValueError("Total must be in the format X.XX")
#         return v

# class ReceiptID(BaseModel):
#     id: str = Field(..., example="adb6b560-0eef-42bc-9d16-df48f30e89b2")

# class Points(BaseModel):
#     points: int = Field(..., example=100)

# def generate_receipt_id() -> str:
#     """Generate a unique ID for a receipt."""
#     return str(uuid.uuid4())

from pydantic import BaseModel, Field
from typing import List
from datetime import date, time
import uuid
import re

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
