from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import date
from app.apis.users import models as users
from ..transactions import models as transaction_models
from app.apis.accounts.models import Account 
from fastapi import HTTPException, status
from sqlalchemy import func


async def get_summary_report(db: AsyncSession, user: users.User, start_date: date, end_date: date) -> dict:
    income_query = select(
        func.sum(transaction_models.Transaction.amount)
    ).where(
        transaction_models.Transaction.recipient_account_id == user.id,
        transaction_models.Transaction.timestamp.between(start_date, end_date)
    )

    expense_query = select(
        func.sum(transaction_models.Transaction.amount)
    ).where(
        transaction_models.Transaction.sender_account_id == user.id,
        transaction_models.Transaction.timestamp.between(start_date, end_date)
    )

    total_income = await db.execute(income_query)
    total_income = total_income.scalar_one_or_none() or 0.0

    total_expense = await db.execute(expense_query)
    total_expense = total_expense.scalar_one_or_none()

    query_ending_balance = select(Account.balance).where(Account.id == user.id)
    ending_balance = await db.execute(query_ending_balance)
    ending_balance = ending_balance.scalar_one_or_none() or 0.0

    if total_income is None or total_expense is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Couldn't find transactions"
        )

    net_flow = total_income - total_expense

    starting_balance = ending_balance - net_flow

    return {
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "starting_balance": starting_balance,
        "ending_balance": ending_balance,
        "total_income": total_income,
        "total_expense": total_expense,
        "net_flow": net_flow,
    }