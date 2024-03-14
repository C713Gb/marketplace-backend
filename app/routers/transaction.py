from fastapi import APIRouter, HTTPException, Depends
from ..models.transaction import Transaction as TransactionModel
from ..models.product import Product as ProductModel
from ..models.bid import Bid as BidModel
from ..models.user import User as UserModel
from ..schemas.transaction_schema import TransactionCreate, TransactionResponse
from ..core.security import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/create", response_model=TransactionResponse)
def create_transaction_from_bid(request_body: TransactionCreate, current_user: UserModel = Depends(get_current_user)):
    bid_id = request_body.bid_id
    bid = BidModel.objects(id=bid_id).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    if str(bid.buyer.id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to purchase this product")

    # Create the transaction based on the bid
    transaction_obj = TransactionModel(
        bid=bid,
    ).save()

    return {
        "id": str(transaction_obj.id),
        "bid_id": str(bid_id),
        "timestamp": transaction_obj.timestamp
    }