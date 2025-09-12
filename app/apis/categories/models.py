from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Enum, DateTime, func
from app.db.base import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User") 
