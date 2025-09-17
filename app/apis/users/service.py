from typing import Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlalchemy.future import select
from app.core import security
from ..accounts.models import Account

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def get_user_by_email(db: AsyncSession, email: str) -> Union[models.User, None]:
	query = select(models.User).where(models.User.email == email)
	result = await db.execute(query)
	return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)

    default_account = Account(user=db_user)
    db.add(default_account)

    await db.commit()
    await db.refresh(db_user)
    
    return db_user

async def get_all_users(db: AsyncSession) -> List[models.User]:
	query = select(models.User)
	result = await db.execute(query)
	return result.scalars().all()


async def delete_user(db: AsyncSession, user_id: int) -> models.User:
	user_to_delete = await db.get(models.User, user_id)
	
	await db.delete(user_to_delete)
	await db.commit()
	return user_to_delete

async def disable_user(db: AsyncSession, user_to_deactivate: models.User) -> models.User | None:
    if not user_to_deactivate.is_active:
        return user_to_deactivate
    
    user_to_deactivate.is_active = False

    db.add(user_to_deactivate)
    await db.commit()
    await db.refresh(user_to_deactivate)

    return user_to_deactivate

async def authenticate_user(db: AsyncSession, email: str, password: str) -> models.User | None:
    user = await get_user_by_email(db, email=email)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user