from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import requests
from sqlalchemy.orm import Session
from database import get_db
from models import User

# Supabase project ID & JWKS endpoint
SUPABASE_PROJECT_ID = "nihcevicnytxaxuxnucs"  # replace with your actual project ID
SUPABASE_JWKS_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1/keys"
jwks = requests.get(SUPABASE_JWKS_URL).json()

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    try:
        header = jwt.get_unverified_header(token)
        kid = header["kid"]

        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if not key:
            raise HTTPException(status_code=401, detail="Public key not found")

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=None,
            options={"verify_exp": True},
        )

        user_id = payload["sub"]
    except Exception as e:
        print("JWT verification error:", e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Check if user exists in local DB
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def get_current_active_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user
