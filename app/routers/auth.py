from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..models.user import User as UserModel
from ..schemas.user_schema import UserCreate, Token
from ..core.security import create_access_token, authenticate_user, get_password_hash, create_refresh_token
from datetime import timedelta

router = APIRouter()

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

@router.post("/register", response_model=Token)
def register_user(user: UserCreate):
    db_user = UserModel.objects(email=user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = UserModel(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role
    ).save()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(new_user.id)}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": str(new_user.id)})
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}
