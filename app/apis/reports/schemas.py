from pydantic import BaseModel
from datetime import date

class ReportSummary(BaseModel):
    period: dict
    starting_balance: float = 0.0
    ending_balance: float = 0.0
    total_income: float = 0.0
    total_expense: float = 0.0
    net_flow: float = 0.0