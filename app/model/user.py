
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship

from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    role = Column(Enum("user", "admin", name="role"), default="user")
    subscription = Column(Enum("free", "premium", name="subscription"), default="free")
    token = Column(Integer, default=100)
    google_id = Column(String, unique=True, nullable=True)
    auth_provider = Column(String, nullable=True)
    last_reset_date = Column(DateTime, default=datetime.utcnow)
    banned = Column(Boolean, default=False)

    predictions = relationship(
        "PredictionHistory", back_populates="user", cascade="all, delete-orphan"
    )
