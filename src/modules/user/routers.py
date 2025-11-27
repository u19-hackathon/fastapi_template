from fastapi import APIRouter

from src.modules.user.schemas import UserRegisterDTO

router = APIRouter(prefix="api/users")


@router.get("/{user_id}")
async def get_user(user_id: int):
    pass


@router.post("")
async def create_user(user_register_dto: UserRegisterDTO):
    pass
