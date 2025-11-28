from fastapi import APIRouter, Depends, HTTPException

from src.core.dependencies import get_jwt_service, get_authentication_header, get_user_service
from src.modules.jwt.schemas import JWTResponseDTO
from src.modules.jwt.services import JWTService
from src.modules.jwt.util import TokenType
from src.modules.user.schemas import UserRegisterDTO, UserResponseDTO, UserLoginDTO
from src.modules.user.services import UserService

user_router = APIRouter(prefix="/api/users")


@user_router.get("/{user_id}")
async def get_user(
        user_id: int,
        user_jwt: str = Depends(get_authentication_header),
        user_service: UserService = Depends(get_user_service),
        jwt_service: JWTService = Depends(get_jwt_service)
) -> UserResponseDTO:
    payload = jwt_service.decode_token(token=user_jwt)
    if payload.get("type"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if int(payload.get("sub", -1)) != user_id:
        raise HTTPException(status_code=403, detail="Not enough rights")

    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponseDTO.model_validate(user)


@user_router.post("/register")
async def register(
        user_register_dto: UserRegisterDTO,
        jwt_service: JWTService = Depends(get_jwt_service),
        user_service: UserService = Depends(get_user_service)
) -> JWTResponseDTO:
    try:
        user = user_service.create_user(user_register_dto)
        if not user:
            raise HTTPException(status_code=400, detail="Email is already in use")
    except ValueError:
        raise HTTPException(status_code=422, detail="Password isn't enough strong")
    except Exception:
        raise HTTPException(status_code=400, detail="Unknown user creation error")
    return JWTResponseDTO(
        user_id=user.id,
        access=jwt_service.create_token(user.id, user.position, TokenType.ACCESS),
        refresh=jwt_service.create_token(user.id, user.position, TokenType.REFRESH)
    )


@user_router.post("/login")
async def login(
        user_register_dto: UserLoginDTO,
        jwt_service: JWTService = Depends(get_jwt_service),
        user_service: UserService = Depends(get_user_service)
) -> JWTResponseDTO:
    try:
        user = user_service.get_user_by_email(user_register_dto.email)
    except ValueError:
        raise HTTPException(status_code=403, detail="Wrong email or password")
    if not user_service.validate_password(user_register_dto.password, user.password):
        raise HTTPException(status_code=403, detail="Wrong email or password")
    return JWTResponseDTO(
        user_id=user.id,
        access=jwt_service.create_token(user.id, user.position, TokenType.ACCESS),
        refresh=jwt_service.create_token(user.id, user.position, TokenType.REFRESH)
    )


@user_router.delete("/{user_id}")
async def delete_user(
        user_id: int,
        user_jwt: str = Depends(get_authentication_header),
        jwt_service: JWTService = Depends(get_jwt_service),
        user_service: UserService = Depends(get_user_service)
) -> None:
    payload = jwt_service.decode_token(token=user_jwt)
    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if payload.get("type"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Unauthorized")
    if int(payload.get("sub", -1)) != user_id:
        raise HTTPException(status_code=403, detail="Not enough rights")
    user_service.delete_user(user_id)
    return None


@user_router.get("/refresh")
async def refresh(
        user_jwt: str = Depends(get_authentication_header),
        jwt_service: JWTService = Depends(get_jwt_service),
        user_service: UserService = Depends(get_user_service)
) -> JWTResponseDTO:
    payload = jwt_service.decode_token(user_jwt)
    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not payload.get("type"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = user_service.get_user_by_id(int(payload.get("sub"), -1))
    return JWTResponseDTO(
        user_id=user.id,
        access=jwt_service.create_token(user.id, user.position, TokenType.ACCESS),
        refresh=jwt_service.create_token(user.id, user.position, TokenType.REFRESH)
    )
