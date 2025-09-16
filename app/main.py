from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from fastapi.responses import HTMLResponse

from app.apis.users.router import router as users_router
from app.apis.auth.router import router as auth_router
from app.apis.transactions.router import router as transaction_router
from app.apis.reports.router import router as report_router
from app.apis.notifications.router import router as notifications_router


swagger_params = {
    "persistAuthorization": True
}

app = FastAPI(
    swagger_ui_parameters=swagger_params
)

origins = [
    "http://localhost",
    "http://localhost:8080", 
    "http://localhost:3000", 
    "http://localhost:8888",
    "null", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return HTMLResponse("Hello world")



app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(transaction_router, prefix="/transaction", tags=["Transaction"])
app.include_router(report_router, prefix="/report", tags=["report"])
app.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])


