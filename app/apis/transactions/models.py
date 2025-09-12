from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Enum, DateTime, func
from app.db.base import Base
from sqlalchemy.orm import relationship

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False) 
    timestamp = Column(DateTime, default=func.now())
    description = Column(String, nullable=True)
    sender_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    recipient_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    category = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category")

    
