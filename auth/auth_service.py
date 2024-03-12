from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, status, Depends
from typing import Annotated
from jose import JWTError, jwt
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from core.database import get_db
from v1.repository import user_repo
from v1.models.users import User
from auth.auth_schemas import TokenResponse
from core.config import get_settings

credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )

settings = get_settings()

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer( tokenUrl = "/api/v1/token" )

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(password, hased_pasword):
    return pwd_context.verify(password, hased_pasword)

def authenticate_user(
    db: Session,
    form_data: OAuth2PasswordRequestForm
):
    db_user = user_repo.find_by_email(db, form_data.username)

    if not db_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "email not found",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "wrong password",
            headers = {"WWW-Authenticate": "Bearer"}
        )

    return db_user

def create_access_token(
    user: User,
    expires_delta: timedelta | None = None
) -> TokenResponse:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15)

    to_encode = {
        "id": user.id,
        "exp": expire
    }

    jwt_encoded = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm = settings.JWT_ALGORITHM)

    model_response = TokenResponse(access_token = jwt_encoded, expires = expire.second)
    return model_response

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db = None   
):

    try:
        data = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        id: str = data.get("id")

        if id is None:
            raise credentials_exception
        
        db = next(get_db())

        user = user_repo.find_by_id(db = db, id = id)

        if user is None:
            raise credentials_exception
        
        if user.is_active is False:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'user not active')
        
        return user.to_dto()
    except JWTError:
        raise credentials_exception
    

def return_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db = None
):
    try:
        data = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        id: str = data.get("id")

        if id is None:
            raise credentials_exception
        
        db = next(get_db())

        user = user_repo.find_by_id(db = db, id = id)

        if user is None:
            raise credentials_exception
        
        if user.is_active is False:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'user not active')
        
        return id
    except JWTError:
        raise credentials_exception