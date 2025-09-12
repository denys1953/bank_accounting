from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class UserRole(str, enum.Enum):
	USER = "user"
	ADMIN = "admin"

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True, index=True)
	hashed_password = Column(String)
	is_active = Column(Boolean, default=True)
	created_at = Column(DateTime, default=func.now())
	updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
	role = Column(Enum(UserRole, name="userrole", native_enum=False), default=UserRole.USER, nullable=False)
	accounts = relationship("Account", back_populates="user")

