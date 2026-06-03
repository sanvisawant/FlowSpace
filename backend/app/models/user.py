from sqlalchemy import Column, String, DateTime, Boolean, func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # mirrors Supabase auth.users.id UUID string
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    welcome_email_sent = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
