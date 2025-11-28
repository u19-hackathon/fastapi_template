# инициализация соединений с базами данных
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.core.config import SQLALCHEMY_DATABASE_URL

Base = declarative_base()

# импорт всех моделей
from src.modules.user.models import User
from src.modules.storage.models import File
from src.modules.storage.models import Source
from src.modules.storage.models import Category
from src.modules.storage.models import Tag
from src.modules.storage.models import FileTag

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_recycle=3600  # закрытие соединений при бездействии
)
session_maker = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)
