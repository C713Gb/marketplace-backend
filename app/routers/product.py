from fastapi import APIRouter, HTTPException
from ..models.product import Product as ProductModel
from ..schemas.product_schema import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate):
    try:
        product_obj = ProductModel(
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            seller=product.seller  # Ensure the seller ID is passed correctly and exists
        ).save()
        return ProductResponse(id=str(product_obj.id), name=product_obj.name, description=product_obj.description, price=product_obj.price, category=product_obj.category, seller=product_obj.seller)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    product_obj = ProductModel.objects(id=product_id).first()
    if product_obj:
        return ProductResponse(id=str(product_obj.id), name=product_obj.name, description=product_obj.description, price=product_obj.price, category=product_obj.category, seller=product_obj.seller)
    else:
        raise HTTPException(status_code=404, detail="Product not found")
