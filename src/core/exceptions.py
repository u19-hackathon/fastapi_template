class ConfigException(Exception):
    """
    Ошибка в конфигурационных данных
    """

class DatabaseConfigException(ConfigException):
    """
    Ошибка загрузки данных о соединении с БД
    """
