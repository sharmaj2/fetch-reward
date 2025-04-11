from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.models import Receipt, ReceiptID, Points
from app.database import get_db_client, SQLiteClient
from app.points import calculate_points

app = FastAPI(
    title="Receipt Processor",
    description="A simple receipt processor",
    version="1.3.0"
)

def get_db():
    """Dependency to get the database connection"""
    return get_db_client()


@app.post("/receipts/process", response_model=ReceiptID, status_code=status.HTTP_200_OK)
async def process_receipt(receipt: Receipt, db: SQLiteClient = Depends(get_db_client)):
    """
    Process a receipt and return its ID
    """
    # Store the receipt in the database
    receipt_id = db.store_receipt(receipt)
    
    # Return the ID
    return {"id": receipt_id}

@app.get("/receipts/{id}/points", response_model=Points)
async def get_points(id: str, db: SQLiteClient = Depends(get_db_client)):
    """
    Get the points for a receipt
    """
    # Check if the receipt exists
    if not db.receipt_exists(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No receipt found for that ID."
        )
    
    # Get the receipt data
    receipt_data = db.get_receipt(id)

    receipt_obj = Receipt.model_validate(receipt_data) #Deserialize receipt_data
    
    # Calculate points
    points = calculate_points(receipt_obj)
    
    # Return the points
    return {"points": points}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "The receipt is invalid."},
    )

# For direct execution
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)