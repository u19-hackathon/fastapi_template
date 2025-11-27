class ConfigException(Exception):
    """
    Ошибка в конфигурационных данных
    """

class JWTConfigException(ConfigException):
    """
    Ошибка в конфигурационных данных jwt
    """

class DatabaseConfigException(ConfigException):
    """
    Ошибка загрузки данных о соединении с БД
    """
