# инициализация соединений с базами данных
from sqlalchemy import create_engine
from .config import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600  # закрытие соединений при бездействии
)

