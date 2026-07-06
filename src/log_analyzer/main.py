import json
import sys
from pathlib import Path
from itertools import islice
from .parser import NginxLogParser
from .stats import LogStatistics
from .config import Config


def main():
    try: 
        Config.validate() #валидируем значения для конфига
        
        print(f"📊 Analyzing log file: {Config.LOG_FILE_PATH}")
        
        parser = NginxLogParser() #парсим данные файла логов
        logs_generator = parser.parse_file_generator(Config.LOG_FILE_PATH)
        
        logs = list(islice(logs_generator, Config.MAX_LINES))#берем из распаршенного файла только первые max_lines строк
        
        print(f"✅ Parsed {len(logs)} log entries") #выдаем длину итогового списка строк
        
        #считаем общую статистику
        stats = LogStatistics(logs)
        summary = stats.get_summary() 
        
        if Config.OUTPUT_FORMAT == 'json': #если json дампим и принтим 
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        else:
            print("\n=== Log Analysis Summary ===")
            print(f"Total requests: {summary['total_requests']}")
            top_ip = summary['top_ips'][0] 
            print(f"Top IP: {top_ip['ip']} ({top_ip['count']} requests)")
            print(f"Errors (4xx/5xx): {summary['errors']}")
            print(f"Status distribution: {summary['status_distribution']}")
            
    except FileNotFoundError: # обработка исключений, нет файла
        print(f"❌ Error: Log file not found: {Config.LOG_FILE_PATH}", file=sys.stderr)
        sys.exit(1)
    except Exception as e: #все остальные исключения 
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    

if __name__ == "__main__": #когда используем как модуль функция выполняется
    main() 