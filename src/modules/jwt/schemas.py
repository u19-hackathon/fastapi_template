from pydantic import BaseModel


class JWTResponseDTO(BaseModel):
    user_id: int
    access: str
    refresh: str
