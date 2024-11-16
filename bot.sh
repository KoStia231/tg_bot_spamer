#!/bin/bash

PROJECT_PATH=$(dirname "$(realpath "$0")")

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