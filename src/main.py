from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.responses import HTMLResponse

from core.dependencies import get_jwt_service
from modules.jwt.service import JWTService
from modules.jwt.util import TokenType

app = FastAPI()


@app.get("/")
async def root():
    html_content = '<h2>Hello gays!</h2>'
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/jwt")
async def jwt(jwt_service: JWTService = Depends(get_jwt_service)):
    """
    Заглушка для проверки работы JWT
    """
    access_token = jwt_service.create_token(1, "Manager", TokenType.ACCESS)
    refresh_token = jwt_service.create_token(1, "Manager", TokenType.REFRESH)
    return {
        "access": access_token,
        "refresh_token": refresh_token
    }
