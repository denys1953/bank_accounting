from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from app.db.sessions import get_db
from app.core.security import get_current_user
from app.apis.permissions import allow_admin_only
from . import schemas, service, models

router = APIRouter(
	# dependencies=[Depends(get_current_user)]
)

@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
	existing_user = await service.get_user_by_email(db=db, email=user_in.email)

	if existing_user:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="User with this email already exists"
		)
	
	new_user = await service.create_user(db=db, user=user_in)
	return new_user

@router.get("/me", response_model=schemas.UserRead)
async def read_current_user(current_user: models.User = Depends(get_current_user)):
	return current_user

@router.delete("/me", response_model=schemas.UserRead)
async def disable_user(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
	await service.disable_user(db=db, user_to_deactivate=current_user)

	return current_user

@router.get("/", response_model=List[schemas.UserRead])
async def get_all_users(
	db: AsyncSession = Depends(get_db), 
	current_admin: models.User = Depends(allow_admin_only)
):
    users = await service.get_all_users(db=db)
    return users

@router.get("/{user_email}", response_model=schemas.UserRead)
async def get_user_by_email(user_email: str, db: AsyncSession = Depends(get_db)):
	user = await service.get_user_by_email(db=db, email=user_email)
	return user

@router.delete("/{user_id}", response_model=schemas.UserRead)
async def delete_user(
	user_id: int, 
	db: AsyncSession = Depends(get_db),
	admin: AsyncSession = Depends(allow_admin_only)
):
	user = await service.delete_user(db=db, user_id=user_id)
	return user