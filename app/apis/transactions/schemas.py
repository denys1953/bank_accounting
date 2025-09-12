from pydantic import BaseModel, PositiveFloat
from datetime import datetime


class TransactionBase(BaseModel):
    amount: PositiveFloat
    description: str | None = None


class TransactionCreate(TransactionBase):
    recipient_account_id: int


class TransactionUpdate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int
    sender_account_id: int
    recipient_account_id: int
    timestamp: datetime

    class Config:
        from_attributes = True 
