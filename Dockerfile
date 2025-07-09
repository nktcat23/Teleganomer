# Базовый образ с Python
FROM python:3.11-slim

# Установка зависимостей для сборки C-библиотек
RUN apt-get update && apt-get install -y gcc

# Установка зависимостей Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода бота
COPY . .

# Команда запуска
CMD ["python", "main.py"]
