from fastapi import APIRouter, Depends, HTTPException

from src.core.dependencies import get_jwt_service, get_authentication_header, get_user_service
from src.modules.jwt.service import JWTService
from src.modules.user.schemas import UserRegisterDTO, UserResponseDTO
from src.modules.user.services import UserService

router = APIRouter(prefix="api/users")


@router.get("/{user_id}")
async def get_user(
        user_id: int,
        user_jwt: str = Depends(get_authentication_header),
        user_service: UserService = Depends(get_user_service),
        jwt_service: JWTService = Depends(get_jwt_service)
):
    payload = jwt_service.decode_token(token=user_jwt)
    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if int(payload.get("sub", -1)) != user_id:
        raise HTTPException(status_code=403, detail="Not enough rights")

    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponseDTO.model_validate(user)


@router.post("")
async def create_user(user_register_dto: UserRegisterDTO):
    pass
