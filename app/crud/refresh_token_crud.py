from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from app.models.models import RefreshToken
from app.exceptions.exceptions import TokenNotFoundException
load_dotenv()

REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

def store_refresh_token(db: Session, user_id: int, token: str,):
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    db_token = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_refresh_token(token: str, db: Session):
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()

    if not db_token: 
        raise TokenNotFoundException(message="Refresh token not found")
    return db_token


def revoke_refresh_token(token: str, db: Session):
    db_token = get_refresh_token(token=token, db=db)
    db_token.revoked = True
    db.commit()
    return db_token

def is_refresh_token_valid(token: str, db: Session):
    try:
      db_token = get_refresh_token(token=token, db=db)

      if db_token.revoked:
        return False
      if db_token.expires_at < datetime.now():
        return False
      return True
    
    except TokenNotFoundException:
       return False

