from fastapi import FastAPI
from app.apis.users.router import router as users_router
from app.apis.auth.router import router as auth_router
from app.apis.transactions.router import router as transaction_router
from app.apis.reports.router import router as report_router

swagger_params = {
    "persistAuthorization": True
}

app = FastAPI(
    swagger_ui_parameters=swagger_params
)

@app.get("/")
async def read_root():
    return {"message": "Hello world!"}


app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(transaction_router, prefix="/transaction", tags=["Transaction"])
app.include_router(report_router, prefix="/report", tags=["report"])

