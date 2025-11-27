# файл конфигураций приложения, загрузка переменных окружения и тп
import os

from sqlalchemy import URL

from core.exceptions import DatabaseConfigException

# подключение к БД
DB_USER = os.environ.get("DB_USER")
DB_USER_PASSWORD = os.environ.get("DB_USER_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

if not all([DB_USER, DB_USER_PASSWORD, DB_NAME, DB_HOST, DB_PORT]):
    raise DatabaseConfigException("Недостаточно данных для подключения к БД")

# dialect+driver://username:password@host:port/database # PyMySQL
SQLALCHEMY_DATABASE_URL = URL.create(
    "mysql+pymysql",
    username=DB_USER,
    password=DB_USER_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)
