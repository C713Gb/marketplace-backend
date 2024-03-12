from fastapi import APIRouter, HTTPException
from mongoengine.errors import NotUniqueError, ValidationError
from passlib.context import CryptContext
from ..models.user import User as UserModel
from ..schemas.user_schema import UserCreate, UserResponse

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

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    user_obj = UserModel.objects(id=user_id).first()
    if user_obj:
        return UserResponse(id=str(user_obj.id), username=user_obj.username, email=user_obj.email, role=user_obj.role)
    else:
        raise HTTPException(status_code=404, detail="User not found")
