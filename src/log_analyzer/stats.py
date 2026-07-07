from collections import Counter


class LogStatistics:
    """Класс для вычисления статистики из логов."""

    def __init__(self, logs: list[dict]) -> None:
        self.logs = logs

    def get_top_ips(self, n: int = 10) -> list[dict]:
        """Подсчет топ n ip по количеству повторений
        на выходе получаем:
        [
            "10.10.10.10": 2,
            "2.2.2.2": 1
        ]
        """

        # пробегаемся по логам(по словарям) и получаем ip:count(словарь)
        ip_counter = Counter(log["ip"] for log in self.logs)

        return [
            {"ip": ip, "count": count}
            # бежим по словарю часто встречающихся(most_common по убыванию выбирает)
            for ip, count in ip_counter.most_common(n)
        ]

    def get_errors_count(self) -> int:
        """Возвращаем количество ошибок (4xx, 5xx)"""

        return sum(1 for log in self.logs if log["status"] >= 400)

    def get_status_distribution(self) -> dict:
        """
        Возвращает распределение по статусам

        Returns:
            Словарь {status: count}
        """
        # получаем {status_code: count}
        status_counter = Counter(log["status"] for log in self.logs)
        return dict(status_counter)

    def get_summary(self) -> dict:
        """
        возвращает краткую сводку по логам

        Returns:
            Словарь с основной статистикой
        """
        if not self.logs:
            return {
                "total_requests": 0,
                "top_ips": [],
                "errors": 0,
                "status_distribution": {},
            }
        top_ips = self.get_top_ips(5)

        return {
            "total_requests": len(self.logs),
            "top_ips": top_ips,
            "errors": self.get_errors_count(),
            "status_distribution": self.get_status_distribution(),
        }
