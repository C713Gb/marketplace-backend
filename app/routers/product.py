from fastapi import APIRouter, HTTPException
from typing import List
from ..models.product import Product as ProductModel
from ..models.user import User as UserModel
from ..schemas.product_schema import ProductCreate, ProductResponse
from ..schemas.user_schema import UserResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate):
    try:
        product_obj = ProductModel(
            name=product.name,
            description=product.description,
            price=product.price,
            seller=product.seller_id
        ).save()
        
        seller_user = UserModel.objects(id=product_obj.seller.id).first()
        seller_response = UserResponse(
            id=str(seller_user.id), 
            username=seller_user.username, 
            email=seller_user.email,
            role=seller_user.role
        )
        
        return ProductResponse(id=str(product_obj.id), name=product_obj.name, description=product_obj.description, price=product_obj.price, seller=seller_response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    product_obj = ProductModel.objects(id=product_id).first()
    if product_obj:
        return ProductResponse(id=str(product_obj.id), name=product_obj.name, description=product_obj.description, price=product_obj.price, seller=product_obj.seller)
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@router.get("/", response_model=List[ProductResponse])
def get_all_products():
    products = ProductModel.objects.all()  # Fetch all products
    product_responses = []

    for product in products:
        # For each product, fetch the seller details
        seller_user = UserModel.objects(id=product.seller.id).first()
        seller_response = UserResponse(
            id=str(seller_user.id), 
            username=seller_user.username, 
            email=seller_user.email,
            role=seller_user.role
        )
        # Append the product info and seller details to the response list
        product_responses.append(
            ProductResponse(
                id=str(product.id),
                name=product.name,
                description=product.description,
                price=product.price,
                seller=seller_response  # Populate seller details in the response
            )
        )

    return product_responses