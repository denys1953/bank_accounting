#!/bin/bash

# Скрипт для запуску проекту
echo "🚀 Запуск FastAPI проекту з Docker..."

# Перевіряємо чи існує .env файл
if [ ! -f .env ]; then
    echo "❌ Файл .env не знайдено!"
    echo "📝 Створюємо приклад файлу .env..."
    cat > .env << EOF
# Database
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword

# Security
SECRET_KEY=59401e7708e861774a7e680abfaf7aafa8b5f33e6c9478390efe7efb636da5e4
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=300
REFRESH_TOKEN_EXPIRE_DAYS=30

# App
DEBUG=False
EOF
    echo "✅ Файл .env створено! Будь ласка, відредагуйте його згідно з вашими налаштуваннями."
    exit 1
fi

# Перевіряємо чи встановлений Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не встановлено!"
    exit 1
fi

# Перевіряємо чи встановлений Docker Compose
if ! command -v docker-compose &> /dev/null && ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose не встановлено!"
    exit 1
fi

echo "🔧 Зупиняємо існуючі контейнери..."
docker compose down 2>/dev/null || docker-compose down 2>/dev/null

echo "🏗️ Збираємо Docker образи..."
docker compose build || docker-compose build

echo "🚀 Запускаємо сервіси..."
docker compose up || docker-compose up
