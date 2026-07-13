from log_analyzer.stats import LogStatistics


class TestLogStatistics:
    """тесты для класса LogStatistics"""

    def test_get_top_ips(self, sample_logs):
        stats = LogStatistics(sample_logs)
        top_ips = stats.get_top_ips(n=3)

        assert len(top_ips) == 3

        assert top_ips[0]["ip"] == "192.168.1.1"  # 3 запроса
        assert top_ips[0]["count"] == 3
        assert top_ips[1]["ip"] == "192.168.1.2"  # 2 запроса
        assert top_ips[1]["count"] == 2

    def test_get_errors_count(self, sample_logs):
        stats = LogStatistics(sample_logs)
        errors = stats.get_errors_count()

        # 404, 500, 403 = 3 ошибки
        assert errors == 3

    def test_get_errors_count_no_errors(self):
        """тестируем подсчет ошибок когда их нет"""
        logs = [
            {"ip": "192.168.1.1", "status": 200},
            {"ip": "192.168.1.2", "status": 201},
            {"ip": "192.168.1.3", "status": 302},
        ]
        stats = LogStatistics(logs)
        errors = stats.get_errors_count()

        assert errors == 0

    def test_get_status_distribution(self, sample_logs):
        """тестируем распределение по статусам"""

        stats = LogStatistics(sample_logs)
        status_distr = stats.get_status_distribution() 

        assert status_distr[200] == 4
        assert status_distr[404] == 1
        assert status_distr[500] == 1
        assert status_distr[403] == 1

    def test_get_summary(self, sample_logs):
        """тестируем полную сводку"""
        stats = LogStatistics(sample_logs)
        summary = stats.get_summary()

        assert len(summary["top_ips"]) == 4
        assert summary["top_ips"][0]["ip"] == "192.168.1.1"
        assert summary["top_ips"][0]["count"] == 3

        assert summary["total_requests"] == 7
        assert summary["errors"] == 3
        assert 200 in summary["status_distribution"]
        assert 404 in summary["status_distribution"]

    def test_get_summary_empty_logs(self):
        """тестируем сводку для пустых логов"""
        stats = LogStatistics([])
        summary = stats.get_summary()

        assert summary["total_requests"] == 0
        assert summary["top_ips"] == []
        assert summary["errors"] == 0
        assert summary["status_distribution"] == {}
