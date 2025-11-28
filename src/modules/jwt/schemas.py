from pydantic import BaseModel


class JWTResponseDTO(BaseModel):
    user_id: str
    access: str
    refresh: str
