# ORM модели для взаимодействия с БД
import enum

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, Enum
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    first_lines = Column(Text)
    file_size = Column(Integer)
    file_type = Column(String(50))
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Внешние ключи
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("source.id"), nullable=False)

    # Связи
    user = relationship("User", back_populates="files")
    category = relationship("Category", back_populates="files")
    source = relationship("Source", back_populates="files")


# Enum для типа откуда отправлены файлы, уровень конфидициальности, уровень приоритета
class SourceType(enum.Enum):
    website = "website"
    email = "email"
    scan = "scan"
    EDO = "EDO"
    ERP = "ERP"


class PriorityLevel(enum.Enum):
    low = 'low'
    normal = 'normal'
    high = 'high'
    critical = 'critical'


class ConfidentialityLevel(enum.Enum):
    open = 'open'
    internal = 'internal'
    confidential = 'confidential'
    strictly_confidential = 'strictly_confidential'


# ORM для откуда файл
class Source(Base):
    __tablename__ = "source"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source_name = Column(String(255), unique=True, nullable=False)
    source_type = Column(Enum(SourceType), nullable=False)

    files = relationship("File", back_populates="source")


# ORM для Категории файла
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_name = Column(String(255), unique=True, nullable=False)
    document_type = Column(String(255), nullable=False)
    priority_level = Column(Enum(PriorityLevel), default=PriorityLevel.normal)
    confidentiality = Column(Enum(ConfidentialityLevel), default=ConfidentialityLevel.internal)
    description = Column(Text)

    files = relationship("File", back_populates="category")
