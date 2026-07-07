import os
from pathlib import Path


class Config:
    """Конфигурация приложения через переменные окружения."""

    # путь к файлу логов
    LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "/var/log/nginx/app_access.log")

    # размер лога для обработки (в строках, для ограничения памяти)
    MAX_LINES = int(os.getenv("MAX_LINES", "100000"))

    # топ N IP для статистики
    TOP_N_IPS = int(os.getenv("TOP_N_IPS", "10"))

    # формат вывода (json или text)
    OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "json")

    # healthcheck endpoint (для Docker)
    HEALTHCHECK_ENABLED = os.getenv("HEALTHCHECK_ENABLED", "true").lower() == "true"

    @classmethod
    def validate(cls):
        """проверяет конфигурацию на корректность"""
        if not Path(cls.LOG_FILE_PATH).exists():
            raise ValueError(f"Log file not found: {cls.LOG_FILE_PATH}")
        if cls.MAX_LINES <= 0:
            raise ValueError("MAX_LINES must be positive")
        if cls.TOP_N_IPS <= 0:
            raise ValueError("TOP_N_IPS must be positive")
