# ORM модели для взаимодействия с БД

from sqlalchemy import String, Column, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


#ORM для юзера
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    organization_name = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    files = relationship("File", back_populates="user")