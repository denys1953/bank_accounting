from app.apis.users.models import UserRole, User
from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user


class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        
        return current_user

allow_admin_only = RoleChecker([UserRole.ADMIN])
allow_user_and_admin = RoleChecker([UserRole.USER, UserRole.ADMIN])