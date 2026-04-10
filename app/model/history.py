from sqlalchemy import Column, Integer, String,  ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model_name = Column(String, nullable=False)
    accuracy = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="predictions")