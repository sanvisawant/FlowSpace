from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.core.config import settings
from pydantic import BaseModel
from typing import Optional
import re
import httpx

router = APIRouter(prefix="/auth", tags=["auth"])

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True

class EmailVerifyRequest(BaseModel):
    email: str

class EmailVerifyResponse(BaseModel):
    is_valid: bool
    is_smtp_valid: bool
    deliverability: str
    autocorrect: str
    message: str

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["id"]
    email = current_user["email"]
    db_user = current_user["db_user"]

    if not db_user:
        # Create user in public database
        db_user = User(
            id=user_id,
            email=email,
            name=email.split("@")[0] if email else "User"
        )
        db.add(db_user)
        try:
            db.commit()
            db.refresh(db_user)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database synchronization error: {str(e)}"
            )
            
    return db_user

@router.post("/verify-email", response_model=EmailVerifyResponse)
async def verify_email(payload: EmailVerifyRequest):
    email = payload.email.strip()
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is required")
    
    # 1. Basic syntax validation via regex
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, email):
        return EmailVerifyResponse(
            is_valid=False,
            is_smtp_valid=False,
            deliverability="UNDELIVERABLE",
            autocorrect="",
            message="Invalid email address format."
        )

    # 2. Gate fallback simulation strictly behind the absence of settings.ABSTRACT_API_KEY
    if not settings.ABSTRACT_API_KEY:
        # Simulated fallback - development testing only
        email_lower = email.lower()
        if "invalid" in email_lower:
            return EmailVerifyResponse(
                is_valid=True,  # valid format
                is_smtp_valid=False,
                deliverability="UNDELIVERABLE",
                autocorrect="",
                message="Mailbox validation failed (simulated invalid mailbox)."
            )
        
        # Simulated autocorrect
        autocorrect_suggestion = ""
        if email_lower.endswith("@gamil.com"):
            autocorrect_suggestion = email[:-9] + "gmail.com"
        elif email_lower.endswith("@yaho.com"):
            autocorrect_suggestion = email[:-8] + "yahoo.com"
            
        return EmailVerifyResponse(
            is_valid=True,
            is_smtp_valid=True,
            deliverability="DELIVERABLE",
            autocorrect=autocorrect_suggestion,
            message="Email verified successfully (simulated fallback)."
        )

    # 3. Real Abstract API call
    try:
        url = "https://emailreputation.abstractapi.com/v1/"
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url, 
                params={"api_key": settings.ABSTRACT_API_KEY, "email": email}, 
                timeout=8.0
            )
            
            if response.status_code != 200:
                # Log or handle rate limiting/bad keys, but fallback to format validation to avoid blocking signups
                return EmailVerifyResponse(
                    is_valid=True,
                    is_smtp_valid=True,
                    deliverability="UNKNOWN",
                    autocorrect="",
                    message=f"Mailbox verification service unavailable (Status {response.status_code})."
                )
                
            data = response.json()
            
            # Extract reputation API deliverability data
            deliv_data = data.get("email_deliverability", {})
            is_valid_format = bool(deliv_data.get("is_format_valid", True))
            is_smtp_valid = bool(deliv_data.get("is_smtp_valid", False))
            deliverability = str(deliv_data.get("status", "UNKNOWN")).upper()
            
            # Generate autocorrect suggestion locally for common domain typos
            email_lower = email.lower()
            autocorrect = ""
            if email_lower.endswith("@gamil.com"):
                autocorrect = email[:-9] + "gmail.com"
            elif email_lower.endswith("@yaho.com"):
                autocorrect = email[:-8] + "yahoo.com"
            
            # Determine if mailbox exists based on SMTP and deliverability
            is_mailbox_exists = is_valid_format and (is_smtp_valid or deliverability == "DELIVERABLE")
            
            if deliverability == "UNDELIVERABLE":
                is_mailbox_exists = False
                
            return EmailVerifyResponse(
                is_valid=is_valid_format,
                is_smtp_valid=is_smtp_valid,
                deliverability=deliverability,
                autocorrect=autocorrect,
                message="Mailbox verified successfully." if is_mailbox_exists else "This mailbox does not exist or is undeliverable."
            )
            
    except Exception as e:
        # Fallback to syntax validity if network fails
        return EmailVerifyResponse(
            is_valid=True,
            is_smtp_valid=True,
            deliverability="UNKNOWN",
            autocorrect="",
            message=f"Mailbox verification service error: {str(e)}."
        )


