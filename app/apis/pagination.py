from typing import Dict
from fastapi import Query

PaginationParams = Dict[str, int]

def get_pagination_params(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
) -> PaginationParams:
    return {"skip": skip, "limit": limit}