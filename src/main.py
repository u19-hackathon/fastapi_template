from fastapi import FastAPI

from src.modules.storage.routers import storage_router, type_controller, tag_controller, counterparty_controller
from src.modules.user.routers import user_router

app = FastAPI()
# /api/users
app.include_router(user_router)
app.include_router(storage_router)
app.include_router(type_controller)

app.include_router(tag_controller)

app.include_router(counterparty_controller)
