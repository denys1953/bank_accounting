from fastapi import APIRouter, Depends, HTTPException, Response, status, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated
from datetime import date

from app.db.sessions import get_db
from app.core.security import get_current_user
from app.apis.permissions import allow_admin_only
from . import schemas, service
from app.apis.users import models as users

from app.core.pdf_generator import create_receipt_pdf_with_reportlab as create_receipt_pdf

from app.apis import transactions

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/summary", response_model=schemas.ReportSummary)
async def get_summary_report(
    db: AsyncSession = Depends(get_db),
    current_user: users.User = Depends(get_current_user),
    start_date: date = Query(default_factory=lambda: date.today().replace(day=1)),
    end_date: date = Query(default_factory=date.today)
):
    transactions = await service.get_summary_report(db=db, user=current_user, start_date=start_date, end_date=end_date)
    return transactions