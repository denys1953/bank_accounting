from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.apis.users.models import *
from app.apis.transactions.models import *
from app.apis.accounts.models import *
from app.apis.categories.models import *
