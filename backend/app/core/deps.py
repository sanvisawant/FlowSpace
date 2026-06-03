import jwt
from jwt import PyJWKClient
from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

_jwks_client = None

def get_jwks_client():
    global _jwks_client
    if _jwks_client is None:
        supabase_url = settings.SUPABASE_URL
        if not supabase_url and "supabase.co" in settings.DATABASE_URL:
            try:
                parts = settings.DATABASE_URL.split("@")
                if len(parts) > 1:
                    host = parts[1].split(":")[0]
                    if host.startswith("db."):
                        ref = host.replace("db.", "")
                        supabase_url = f"https://{ref}"
            except Exception:
                pass
        if not supabase_url:
            supabase_url = "https://hpvrxkufpmvuweiptsqr.supabase.co"
            
        jwks_url = f"{supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json"
        _jwks_client = PyJWKClient(jwks_url)
    return _jwks_client

async def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected: 'Bearer <token>'"
        )
    token = authorization.replace("Bearer ", "")
    try:
        # Extract unverified header to determine key algorithm
        header = jwt.get_unverified_header(token)
        alg = header.get("alg", "HS256")
        
        if alg == "ES256":
            jwks_client = get_jwks_client()
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            key = signing_key.key
        else:
            key = settings.SUPABASE_JWT_SECRET
            
        payload = jwt.decode(
            token,
            key,
            algorithms=[alg],
            options={"verify_aud": False}
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload: missing sub claim"
            )
        # Fetch user from local db
        db_user = db.query(User).filter(User.id == user_id).first()
        return {
            "id": user_id,
            "email": payload.get("email"),
            "db_user": db_user
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        import logging
        logging.getLogger(__name__).error(f"JWT Verification Failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
