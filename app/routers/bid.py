from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..core.security import get_current_user
from ..models.user import User as UserModel
from ..models.product import Product as ProductModel
from ..models.bid import Bid as BidModel
from ..schemas.bid_schema import BidCreate, BidResponse, BidUpdate

router = APIRouter(prefix="/bids", tags=["bids"])

@router.post("/", response_model=BidResponse)
def create_bid(bid: BidCreate, current_user: UserModel = Depends(get_current_user)):
    product = ProductModel.objects(id=bid.product_id).first()
    print("product ==> ", product)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if str(product.seller.id) == str(current_user.id):
        raise HTTPException(status_code=400, detail="Seller cannot bid on their own product")
    
    bid_obj = BidModel(
        product=product,
        buyer=current_user,
        seller=product.seller,
        amount=bid.amount,
    ).save()
    return {
        "id": str(bid_obj.id),
        "product_id": str(bid_obj.product.id),
        "buyer_id": str(bid_obj.buyer.id),
        "seller_id": str(bid_obj.seller.id),
        "amount": bid_obj.amount,
        "status": bid_obj.status,
        "timestamp": bid_obj.timestamp,
    }

@router.put("/{bid_id}", response_model=BidResponse)
def update_bid(bid_id: str, bid_update: BidUpdate, current_user: UserModel = Depends(get_current_user)):
    bid_obj = BidModel.objects(id=bid_id).first()
    if not bid_obj:
        raise HTTPException(status_code=404, detail="Bid not found")
    if str(bid_obj.buyer.id) != str(current_user.id) and str(bid_obj.seller.id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this bid")
    
    bid_obj.update(**bid_update.dict(exclude_unset=True))
    bid_obj.reload()  # Reload to reflect the updates
    return bid_obj.to_mongo().to_dict()

@router.get("/product/{product_id}", response_model=List[BidResponse])
def list_bids_for_product(product_id: str, current_user: UserModel = Depends(get_current_user)):
    bids = BidModel.objects(product=product_id)
    return list(map(lambda bid: bid.to_mongo().to_dict(), bids))

@router.get("/suggest/{product_id}", response_model=float)
def suggest_bid_amount(product_id: str):
    accepted_bids = BidModel.objects(product=product_id, status='accepted')
    if accepted_bids:
        average_bid = sum(bid.amount for bid in accepted_bids) / len(accepted_bids)
        return round(average_bid, 2)  # Suggested amount based on average of accepted bids
    else:
        return 0.0  # Default suggestion if no accepted bids exist
    
@router.get("/latest/{product_id}", response_model=BidResponse)
def get_latest_bid_for_product(product_id: str, current_user: UserModel = Depends(get_current_user)):
    latest_bid = BidModel.objects(product=product_id).order_by('-timestamp').first()
    if not latest_bid:
        raise HTTPException(status_code=404, detail="No bids found for this product")

    return {
        "id": str(latest_bid.id),
        "product_id": str(latest_bid.product.id),
        "buyer_id": str(latest_bid.buyer.id),
        "seller_id": str(latest_bid.seller.id),
        "amount": latest_bid.amount,
        "status": latest_bid.status,
        "timestamp": latest_bid.timestamp
    }

@router.post("/{bid_id}/accept")
def accept_bid(bid_id: str, current_user: UserModel = Depends(get_current_user)):
    bid = BidModel.objects(id=bid_id).first()
    if not bid or str(bid.seller.id) != str(current_user.id):
        raise HTTPException(status_code=404, detail="Bid not found or not authorized")
    
    bid.status = "accepted"
    bid.save()
    return {"message": "Bid accepted successfully"}

@router.post("/{bid_id}/reject")
def reject_bid(bid_id: str, current_user: UserModel = Depends(get_current_user)):
    bid = BidModel.objects(id=bid_id).first()
    if not bid or str(bid.seller.id) != str(current_user.id):
        raise HTTPException(status_code=404, detail="Bid not found or not authorized")
    
    bid.status = "rejected"
    bid.save()
    return {"message": "Bid rejected successfully"}

@router.post("/{bid_id}/counteroffer")
def counteroffer_bid(bid_id: str, counter_offer_amount: float, current_user: UserModel = Depends(get_current_user)):
    bid = BidModel.objects(id=bid_id).first()
    if not bid or str(bid.seller.id) != str(current_user.id):
        raise HTTPException(status_code=404, detail="Bid not found or not authorized")
    
    bid.status = "counteroffer"
    bid.counterOfferAmount = counter_offer_amount
    bid.save()
    return {"message": "Counteroffer made successfully"}