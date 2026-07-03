#!/bin/bash
# Генерируем трафик на nginx для наполнения логов

BASE_URL="http://localhost:8080"
ITERATIONS=${1:-100} #берет первую введенную переменную и проверяет ее значение, по дефолту 100

echo "🚀 Generating $ITERATIONS requests to $BASE_URL"

for i in $(seq 1 $ITERATIONS); do
    # Разные endpoints для разных статусов
    case $((RANDOM % 10)) in
        0|1|2|3|4|5) #если выпадает от 0 до 5, то успешный запрос
        # 60% успешных запросов
            curl -s "$BASE_URL/api/users" > /dev/null
            ;;
        6|7)
            # 20% 404
            curl -s "$BASE_URL/notfound/$RANDOM" > /dev/null
            ;;
        8)
            # 10% 500
            curl -s "$BASE_URL/error" > /dev/null
            ;;
        9)
            # 10% 403
            curl -s "$BASE_URL/forbidden" > /dev/null
            ;;
    esac

    # Небольшая пауза
    sleep 0.01
done

echo "✅ Done! Check logs with: docker-compose exec nginx cat /var/log/nginx/access.log"