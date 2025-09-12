from fastapi import APIRouter, Depends, HTTPException, Response, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from app.db.sessions import get_db
from app.core.security import get_current_user
from app.apis.permissions import allow_admin_only
from . import schemas, service, models
from app.apis.users import models as users

from app.core.pdf_generator import create_receipt_pdf_with_reportlab as create_receipt_pdf

from app.apis import transactions

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post("/create", response_model=schemas.TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_in: schemas.TransactionCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    new_transaction = await service.create_transaction(db=db, transaction=transaction_in, sender_id=current_user.id)

    return new_transaction
    
@router.get("/{id}", response_model=schemas.TransactionRead)
async def get_transaction_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    transaction = await service.get_transaction_by_id(db=db, transaction_id=id, user=current_user)

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    return transaction

@router.get("/", response_model=List[schemas.TransactionRead])
async def get_all_transactions(
    db: AsyncSession = Depends(get_db),
    current_admin: users.User = Depends(allow_admin_only)
):
    transactions = await service.get_all_transactions(db=db)
    return transactions

@router.delete("/{transaction_id}", response_model=schemas.TransactionRead)
async def delete_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: users.User = Depends(get_current_user),
):
    transaction_to_delete = await service.get_transaction_by_id(
        db=db, 
        user=current_user, 
        transaction_id=transaction_id
    )

    if not transaction_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    await db.delete(transaction_to_delete)
    await db.commit()

    return transaction_to_delete

@router.get("/{transaction_id}/receipt", response_model=schemas.TransactionRead)
async def download_receipt(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: users.User = Depends(get_current_user)
):
    transaction = await service.get_transaction_by_id(transaction_id=transaction_id, db=db, user=current_user)

    pdf_bytes = create_receipt_pdf(transaction=transaction)

    if not pdf_bytes:
        raise HTTPException(status_code=500, detail="Error while generating receipt")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="receipt_{transaction.id}.pdf"'
        }
    )
    
