#!/bin/bash

PROJECT_PATH=$(dirname "$(realpath "$0")")

VENV_PATH="$PROJECT_PATH/.venv/bin/activate"
MAIN_FILE="src/main.py"

echo "Запуск скрипта"

cd "$PROJECT_PATH" || exit

source "$VENV_PATH"

export PYTHONPATH="$PROJECT_PATH"

python "$MAIN_FILE"

deactivate

echo "Процесс завершен."