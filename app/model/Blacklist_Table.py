from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.database import Base

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    token = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)