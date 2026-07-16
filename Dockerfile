FROM python:3.14-slim AS builder

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml README.md ./

#создаем окружение внутри .venv
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

#ставим зависимости
RUN poetry install --only main --no-interaction --no-ansi --no-root

#копируем проект
COPY src/ ./src/ 

#ставим проект как пакет
RUN poetry install --only main --no-interaction --no-ansi



FROM python:3.14-slim AS production


LABEL maintainer="dmitriistrekalin@gmail.com"
LABEL description="Nginx log analyzer"
LABEL version="1.0.0"

WORKDIR /app


#копируем окружение и исходный код
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

#активируем окружение и передаем стандартные переменные
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LOG_FILE_PATH=/var/log/nginx/access.log \
    OUTPUT_FORMAT=json

#пользователя appuser без суперправ и группу appgroup + nginx файлы и права на них
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser && \
    mkdir -p /var/log/nginx && \ 
    chown -R appuser:appgroup /var/log/nginx && \
    chown -R appuser:appgroup /app

#меняем пользователя 
USER appuser

#базовый чек контейнера, ставим таймауты, время, команду для проверки, если вернет что то кроме 0, значит контейнер с ошибкой
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.log_analyzer.main import main" || exit 1 

#вход, запускаем приложение
ENTRYPOINT ["python", "-m", "src.log_analyzer.main"]