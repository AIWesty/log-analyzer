import pytest
from log_analyzer.parser import NginxLogParser


class TestNginxLogParser:
    """Тесты для класса NginxLogParser"""
    
    
    def setup_method(self):
        """создаем парсер перед каждым тестом"""
        self.parser = NginxLogParser()    
        
    def test_parse_line_valid(self):
        """тест парсинга валидной строки"""
        
        line = '192.168.1.1 - - [01/Jul/2026:10:00:00 +0000] "GET /api/health HTTP/1.1" 200 123 "-" "curl/7.68.0"'
        result = self.parser.parse_line(line)
        
        assert result is not None
        assert result['ip'] == '192.168.1.1'
        assert result['method'] == 'GET'
        assert result['status'] == 200
        assert result['method'] == 'GET'
        assert result['url'] == '/api/health'
        assert result['bytes'] == 123
    
    def test_parse_line_invalid(self): 
        """тест парса невалидной строки"""
        line = "INVALID LOG LINE"
        result = self.parser.parse_line(line)
        
        assert result is None
    
    # здесь передаем кортежи в виде statuscode, expected    
    @pytest.mark.parametrize("status_code,expected", [
        ("200", 200),
        ("404", 404),
        ("500", 500),
        ("201", 201) ])
    def test_parse_different_statuses(self, status_code, expected):
        
        line = f'192.168.1.1 - - [01/Jul/2026:10:00:00 +0000] "GET / HTTP/1.1" {status_code} 123 "-" "curl/7.68.0"'
        result = self.parser.parse_line(line)
        
        assert result is not None
        assert result['status'] == expected
        
    def test_parse_file (self, sample_log_path):
        
        logs = list(self.parser.parse_file_generator(str(sample_log_path))) # превращаем обьект Path в строку пути, затем оборачиваем генератор в список
        
        assert len(logs) == 7 #колво элементов
        
        assert logs[0]['ip'] == '192.168.1.1' #первый словарь, первый ключ 
        assert logs[0]['status'] == 200 # первый словарь ключ status
        
        statuses = [log.get('status') for log in logs]
        assert 'INVALID' not in statuses
        
        ips = [log['ip'] for log in logs]
        assert '192.168.1.1' in ips
        assert '192.168.1.2' in ips
        assert '192.168.1.3' in ips
        assert '192.168.1.4' in ips
    
    def test_parse_file_empty_lines(self, tmp_path):
        """тест парса файла с путыми строками"""
        log_file = tmp_path / "empty.log"
        log_file.write_text("\n\n\n")
        
        logs = self.parser.parse_file_generator(log_file)
        assert logs is None 
        
        