from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.modules.storage.routers import storage_router, tag_controller, counterparty_controller, save_file_controller
from src.modules.user.routers import user_router

app = FastAPI()
# /api/users
app.include_router(user_router)
app.include_router(storage_router)
app.include_router(tag_controller)

app.include_router(counterparty_controller)

app.include_router(save_file_controller)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:80",
        "http://localhost:3000",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
