#!/bin/bash
SCRIPT_NAME="main.py"

# Проверяем, запущен ли скрипт
if pgrep -f "$SCRIPT_NAME" >/dev/null; then
  echo "Завершение скрипта $SCRIPT_NAME..."
  pkill -f "$SCRIPT_NAME"
  sleep 1 # Небольшая пауза перед перезапуском
fi

# Запускаем скрипт
echo "Запуск скрипта $SCRIPT_NAME..."
python3 "$SCRIPT_NAME" &
