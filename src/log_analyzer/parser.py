import re

from typing import Optional
from datetime import datetime



class NginxLogParser: 
    """Парсер логов nginx в access формате"""
    
    
    # Пример строки: 192.168.1.1 - - [01/Jul/2026:12:00:00 +0000] "GET /api/health HTTP/1.1" 200 123 "-" "curl/7.68.0"
    LOG_PATTERN = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)' #ip адрес
        r'\s+-\s+-\s+' # identity, user (обычно -)
        r'\[(?P<timestamp>.+)\]s+' #timestamp, ищет \[]\ скобки и символы внутри
        r'"(?P<method>\w+)\s+(?P<url>[^\s]+)\s+(?P<protocol>[^"]+)"\s+' # метод + пробел + все символы кроме пробела, все кроме "", и пробел
        r'(?P<status>\d{3})\s'# 3цифры и пробел
        r'(?P<bytes>\d+)\s+' #цифры 
        r'"(?P<referer>[^"]*)"\s+' # referer
        r'"(?P<user_agent>[^"]*)"'  # user agent
    )
    
    
    