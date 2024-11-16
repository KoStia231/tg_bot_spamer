#!/bin/bash

ENV_FILE=".env"

if [ -f "$ENV_FILE" ]; then
    echo "Загрузка переменных из .env..."
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo "Ошибка: файл .env не найден!"
    exit 1
fi

if [ -z "$PROJECT_PATH" ]; then
    echo "Ошибка: PROJECT_PATH не задан в .env файле!"
    exit 1
fi

VENV_PATH="$PROJECT_PATH/.venv/bin/activate"

MAIN_FILE="main.py"

while true
do
    echo "Запуск main.py..."

    cd "$PROJECT_PATH" || exit

    source "$VENV_PATH"

    python "$MAIN_FILE"

    deactivate

    echo "Процесс завершен. Перезапуск через 2 секунд..."
    sleep 2
done