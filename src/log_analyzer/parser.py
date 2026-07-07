import re
from typing import Iterator, Optional

from tqdm import tqdm


class NginxLogParser: 
    """Парсер логов nginx в access формате"""
    
    
    # Пример строки: 192.168.1.1 - - [01/Jul/2026:12:00:00 +0000] \
    # "GET /api/health HTTP/1.1" 200 123 "-" "curl/7.68.0"
    # регулярный шаблон компилируем один раз 
    LOG_PATTERN = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)' #ip адрес
        r'\s+-\s+-\s+' # identity, user (обычно -)
        r'\[(?P<timestamp>.+)\]\s+' #timestamp, ищет \[]\ скобки и символы внутри
        # метод + пробел + все символы кроме пробела, все кроме "", и пробел    
        r'"(?P<method>\w+)\s+(?P<url>[^\s]+)\s+(?P<protocol>[^"]+)"\s+' 
        r'(?P<status>\d{3})\s'# 3цифры и пробел
        r'(?P<bytes>\d+)\s+' #цифры 
        r'"(?P<referer>[^"]*)"\s+' # referer
        r'"(?P<user_agent>[^"]*)"'  # user agent
    )
    
    def parse_line(self, line: str) -> Optional[dict]:
        """Парсим одну строку лога
            Args: line - строка лога
            Returns: словарь с данными лога или None 
        """
        #применяем шаблон к пришедшей строке
        #strip() ищет пробелы с обеих сторон, rstrip('\n\r')\
        # убирает только переносы строк
        match = self.LOG_PATTERN.match(line.rstrip('\n\r'))
        if not match: #если строка не попала под шаблон вернем none 
            return None 
        
        #собирает словарь с данными по ключам \
        # из совпавшей строки, которые указывали в <>
        return { 
            'ip': match.group('ip'),
            'timestamp': match.group('timestamp'),
            'method': match.group('method'),
            'url': match.group('url'),
            'protocol': match.group('protocol'),
            'status': int(match.group('status')), 
            'bytes': int(match.group('bytes')),
            'referer': match.group('referer'),
            'user_agent': match.group('user_agent')
        
        }
        
        
        
    def parse_file_generator(self, filepath: str) -> Iterator[dict]: 
        """Парсим полный файл, делаем при помощи генератора, чтобы экономить память
            Args: filepath - str
            Returns: список словарей с данными
        """
        with open(filepath, 'r', encoding='utf8') as logfile:
            with tqdm(desc="Parsing logs", unit=" lines") as pbar:
                for line in logfile: # идем построчно по файлу
                    data = self.parse_line(line) #парсим каждую строчку
                    pbar.update(1) # обновляем счетчик строк 
                    if data: 
                        #отдаем результат если строчка сметчилась, не сохраняем в память
                        yield data 
    