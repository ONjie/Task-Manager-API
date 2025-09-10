from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate, UserRead, Token, RefreshRequest
from app.database.database import get_db, db_dependency
from app.crud.user_crud import create_user, get_user
from app.crud.refresh_token_crud import (
   store_refresh_token, 
   is_refresh_token_valid, 
   revoke_refresh_token
   )
from app.auth.auth import (
   get_hashed_password, 
   authenticate_user, 
   create_access_token, 
   create_refresh_token,
   get_current_user_by_refresh_token
   )
from app.exceptions.exceptions import (
   UserNotFoundException, 
   InvalidCredentialsException, 
   InvalidPasswordException,
   TokenNotFoundException
   )


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user: UserCreate, db: db_dependency):
    try:
      db_user = get_user(email=user.email, db=db)
      if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    except UserNotFoundException:
     user.password = get_hashed_password(password=user.password)
     return create_user(user=user, db=db)


@router.post('/login', response_model= Token)
async def login_endpoint(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
         user = authenticate_user(db=db, email=form_data.username, password=form_data.password)
         access_token = create_access_token(data={"sub":user.email})
         refresh_token = create_refresh_token(data={"sub":user.email})

         store_refresh_token(db=db, user_id=user.id, token=refresh_token)

         return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    except (
       InvalidCredentialsException, 
       InvalidCredentialsException, 
       UserNotFoundException,
       InvalidPasswordException
       ) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message, 
            headers={"WWW-Authenticate": "Bearer"},
            )
    
@router.post("/refresh", response_model=Token)
async def refresh_token_endpoint(
    body: RefreshRequest,
   db: db_dependency
   ):
   
   try:
        refresh_token = body.refresh_token

        user = await get_current_user_by_refresh_token(refresh_token=refresh_token, db=db)

        if not is_refresh_token_valid(db=db, token=refresh_token):
           raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token", 
            headers={"WWW-Authenticate": "Bearer"},
            )

        revoke_refresh_token(db=db, token=refresh_token)
        new_refresh_token = create_refresh_token({"sub": user.email})
        store_refresh_token(db, user_id=user.id, token=new_refresh_token)

        new_access_token = create_access_token({"sub": user.email})

        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )
   except (UserNotFoundException, InvalidCredentialsException):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
   


@router.post("/logout")
async def logout_endpoint(refresh_token: str, db: Session = Depends(get_db)):
    try: 
     revoke_refresh_token(db=db, token=refresh_token)
     return {"message": "Successfully logged out"}
    except TokenNotFoundException as e:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
