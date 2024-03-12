from fastapi import APIRouter, HTTPException
from ..models.transaction import Transaction as TransactionModel
from ..schemas.transaction_schema import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate):
    try:
        transaction_obj = TransactionModel(
            buyer=transaction.buyer,
            product=transaction.product,
            quantity=transaction.quantity,
            timestamp=transaction.timestamp  # Optional, defaults to current time if not provided
        ).save()
        return TransactionResponse(id=str(transaction_obj.id), buyer=transaction_obj.buyer, product=transaction_obj.product, quantity=transaction_obj.quantity, timestamp=transaction_obj.timestamp)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: str):
    transaction_obj = TransactionModel.objects(id=transaction_id).first()
    if transaction_obj:
        return TransactionResponse(id=str(transaction_obj.id), buyer=transaction_obj.buyer, product=transaction_obj.product, quantity=transaction_obj.quantity, timestamp=transaction_obj.timestamp)
    else:
        raise HTTPException(status_code=404, detail="Transaction not found")
