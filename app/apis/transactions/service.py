from typing import Union, List
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlalchemy.future import select
from app.core import security
from . import models, schemas
from app.apis.users import models as users
from ..users.models import User, UserRole 
from app.apis.accounts.models import Account 
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from ..pagination import PaginationParams
from app.core.websocket_manager import manager as ws_manager 


async def create_transaction(db: AsyncSession, transaction: schemas.TransactionCreate, sender_id: int) -> models.Transaction:
    db_transaction = models.Transaction(
        amount=transaction.amount,
        description=transaction.description,
        sender_account_id=sender_id,
        recipient_account_id=transaction.recipient_account_id
    )



    sender = await db.get(Account, sender_id)
    recipient = await db.get(Account, transaction.recipient_account_id)
    
    if not sender:
        raise HTTPException(status_code=400, detail="Sender account not found.")

    if not recipient:
        raise HTTPException(status_code=400, detail=f"Recipient user has no account.")

    if sender.id == recipient.id:
        raise HTTPException(status_code=400, detail="Cannot send money to yourself.")

    await db.refresh(sender, with_for_update=True)
    await db.refresh(recipient, with_for_update=True)

    if sender.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds.")

    sender.balance -= transaction.amount
    recipient.balance += transaction.amount


    db.add(db_transaction)
    db.add(sender)
    db.add(recipient)

    await db.commit()
    await db.refresh(db_transaction)

    notification_payload = {
        "type": "NEW_TRANSACTION",
        "data": {
            "transaction_id": db_transaction.id,
            "amount": db_transaction.amount,
            "sender_email": sender.user.email,
            "timestamp": db_transaction.timestamp.isoformat()
        }
    }

    await ws_manager.send_personal_message(notification_payload, user_id=recipient.id)


    return db_transaction

async def get_transaction_by_id(db: AsyncSession, user: users.User, transaction_id: int) -> models.Transaction | None:
    query = (
        select(models.Transaction)
        .where(models.Transaction.id == transaction_id)
        .options(
            selectinload(models.Transaction.sender_account).selectinload(Account.user),
            selectinload(models.Transaction.recipient_account).selectinload(Account.user)
        )
    )    
    result = await db.execute(query)

    transaction = result.scalar_one_or_none()

    if not transaction:
        return None

    if user.role == UserRole.ADMIN:
        return transaction

    if transaction and transaction.sender_account_id == user.id:
        return transaction
    
    return None

async def get_all_transactions(db: AsyncSession, pagination: PaginationParams) -> List[models.Transaction]:
    query = select(models.Transaction).offset(pagination["skip"]).limit(pagination["limit"])
    result = await db.execute(query)
    return result.scalars().all()

async def delete_transaction(db: AsyncSession, user_id, user_role) -> models.Transaction:
    pass

