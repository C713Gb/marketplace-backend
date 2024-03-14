from fastapi import APIRouter, HTTPException, Depends
from mongoengine.errors import NotUniqueError, ValidationError
from passlib.context import CryptContext
from typing import List
from ..models.user import User as UserModel
from ..schemas.user_schema import UserCreate, UserResponse
from ..core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

# Instantiate the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    try:
        # Hash the password before saving it to the database
        hashed_password = pwd_context.hash(user.password)
        user_obj = UserModel(
            username=user.username,
            email=user.email,
            password=hashed_password,  # Use the hashed password
            role=user.role
        ).save()
        return UserResponse(id=str(user_obj.id), username=user_obj.username, email=user_obj.email, role=user_obj.role)
    except NotUniqueError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

# @router.get("/{user_id}", response_model=UserResponse)
# def get_user(user_id: str):
#     user_obj = UserModel.objects(id=user_id).first()
#     if user_obj:
#         return UserResponse(id=str(user_obj.id), username=user_obj.username, email=user_obj.email, role=user_obj.role)
#     else:
#         raise HTTPException(status_code=404, detail="User not found")

@router.get("/", response_model=List[UserResponse])
def get_all_users():
    users = UserModel.objects.all()
    return [UserResponse(id=str(user.id), username=user.username, email=user.email, role=user.role) for user in users]

@router.get("/me", response_model=UserResponse)
async def get_current_user_details(current_user: UserModel = Depends(get_current_user)):
    user_response = UserResponse(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        role=current_user.role
    )
    return user_response