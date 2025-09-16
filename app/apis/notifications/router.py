# app/apis/notifications/router.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.core.websocket_manager import manager
from app.core.security import get_current_user, get_current_user_ws
from app.apis.users.models import User

router = APIRouter()

@router.websocket("/ws/notifications")
async def websocket_notifications_endpoint(
    websocket: WebSocket,
    current_user: User = Depends(get_current_user_ws)
):
    user_id = current_user.id
    await manager.connect(websocket, user_id)
    print(f"User {user_id} has connected to the notifications.")


    try:
        while True:
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        print(f"User {user_id} has disconnected")