from pathlib import Path

import pytest


@pytest.fixture
def sample_log_path() -> Path: 
    """путь к тестовому логу"""
    return Path(__file__).parent / "fixtures" / "sample.log"


@pytest.fixture
def sample_logs() -> list[dict]:
    """готовые распарсенные логи для проверки статистики"""
    return [
        {'ip': '192.168.1.1', 'status': 200, 'bytes': 123, 'method': 'GET'},
        {'ip': '192.168.1.2', 'status': 200, 'bytes': 456, 'method': 'POST'},
        {'ip': '192.168.1.1', 'status': 404, 'bytes': 78, 'method': 'GET'},
        {'ip': '192.168.1.3', 'status': 200, 'bytes': 123, 'method': 'GET'},
        {'ip': '192.168.1.1', 'status': 500, 'bytes': 0, 'method': 'DELETE'},
        {'ip': '192.168.1.2', 'status': 200, 'bytes': 123, 'method': 'GET'},
        {'ip': '192.168.1.4', 'status': 403, 'bytes': 89, 'method': 'PUT'},
    ]