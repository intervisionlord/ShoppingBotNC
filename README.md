# 🛒 ShoppingBotNC - Модульный Telegram Бот

<center>

[![Pylint](https://github.com/intervisionlord/ShoppingBotNC/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/intervisionlord/ShoppingBotNC/actions/workflows/pylint.yml)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![Last Commit](https://img.shields.io/github/last-commit/intervisionlord/ShoppingBotNC)

![Aiogram](https://img.shields.io/badge/aiogram-3.x-00aced?logo=telegram&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.120.0-009688?logo=fastapi&logoColor=white)
![Loguru](https://img.shields.io/badge/loguru-0.7.3-4B275F)

![License](https://img.shields.io/badge/license-GPL3-blue)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/intervisionlord/ShoppingBotNC)

</center>

Минимально рабочая версия каркаса для будущего Telegram бота с модульной архитектурой на Python.

* ![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/intervisionlord/ShoppingBotNC)
* **📋 [CHANGELOG](CHANGELOG.md)**

---
- [🚀 Особенности](#-особенности)
- [📁 Структура проекта](#-структура-проекта)
- [⚙️ Быстрый старт](#️-быстрый-старт)
    - [1. Клонирование и настройка](#1-клонирование-и-настройка)
    - [2. Настройка окружения](#2-настройка-окружения)
    - [3. Установка зависимостей](#3-установка-зависимостей)
    - [4. Запуск](#4-запуск)
- [🛠 Команды бота](#-команды-бота)
- [🌐 API Эндпоинты](#-api-эндпоинты)
- [🔧 Конфигурация](#-конфигурация)
    - [SSL настройки](#ssl-настройки)
- [🚀 Развертывание](#-развертывание)
    - [Локальная разработка](#локальная-разработка)
    - [Продакшен с Docker](#продакшен-с-docker)
        - [С поддержкой отдельного SSL](#с-поддержкой-отдельного-ssl)
- [🔄 Webhook настройка](#-webhook-настройка)
- [🤝 Разработка](#-разработка)
    - [Добавление новых команд](#добавление-новых-команд)
    - [Добавление API эндпоинтов](#добавление-api-эндпоинтов)
- [📄 Лицензия](#-лицензия)


## 🚀 Особенности

* **Модульная архитектура** - Чистая структура проекта для легкого масштабирования
* **FastAPI** - Современный асинхронный веб-фреймворк
* **Aiogram 3.x** - Актуальная версия фреймворка для Telegram ботов
* **Webhook поддержка** - Готовая конфигурация для продакшена

## 📁 Структура проекта

```

├── .env.example                # Пример Конфигурации
├── CHANGELOG.md
├── config
│   └── settings.py             # Настройки приложения
├── core.py                     # Ядро бота
├── handlers                    # Обработчики
│   ├── bot_routes              # Обработчики команд бота
│   │   ├── __init__.py
│   │   ├── base_routes.py      # Основноые команды
│   │   └── nc_deck_routes.py   # Команды для NC Deck
│   ├── handler_bot.py          # Основной хендлер бота
│   ├── handler_logging.py      # Логирование
│   ├── handler_nc_deck.py      # Получение досок NC
│   ├── handler_requests.py     # Отправка запросов в NC
│   └── handler_server.py       # Сервер API
├── LICENSE
├── main.py                     # Основной файл запуска
├── models                      # Модели данных
│   └── model_board.py          # Модель досок
├── README.md
├── requirements.txt            # Зависимости
└── routes
    ├── routes_base.py          # Основные роуты FastAPI
    └── routes_webhook.py       # Роуты вебхука
```

## ⚙️ Быстрый старт
### 1. Клонирование и настройка
```shell
git clone <your-repo-url>
cd shoppingbot
cp .env.example .env
```

### 2. Настройка окружения

Отредактируйте файл `.env`:
```shell
BOT_TOKEN="your_telegram_bot_token_here"

# Для разработки
HOST="0.0.0.0"
PORT="8443"
LOG_LEVEL="INFO"

# Для продакшена
WEBHOOK_HOST="https://yourdomain.com"
SSL_ENABLED=True
SSL_KEY_PATH="/path/to/private.key"
SSL_CERT_PATH="/path/to/certificate.crt"
```

### 3. Установка зависимостей
```shell
pip install -r requirements.txt
```

### 4. Запуск
```shell
python main.py
```

## 🛠 Команды бота

* **/start** - Запуск бота
* **/help** - Список команд
* **/test** - Тестовая команда
* **/about** - О боте
* **test** (текстовое сообщение) - Проверка текстовых хендлеров

## 🌐 API Эндпоинты

* `GET /` - Корневой эндпоинт
* `GET /api` - Корень API
* `GET /api/health` - Проверка здоровья
* `GET /api/test` - Тестовый эндпоинт
* `POST /webhook` - Webhook для Telegram
* `GET /webhook` - Отладочная информация о вебхуке

## 🔧 Конфигурация
```shell
WEBHOOK_HOST="https://yourdomain.com"
SSL_ENABLED=True
```

### SSL настройки

Для локального SSL используйте:
```shell
SSL_ENABLED=True
SSL_KEY_PATH="./private.key"
SSL_CERT_PATH="./certificate.crt"
```

## 🚀 Развертывание
### Локальная разработка
```shell
python main.py
```

### Продакшен с Docker
```dockerfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

#### С поддержкой отдельного SSL

* Сгенерируйте SSL сертификаты
* Укажите пути в `.env`
* Установите `WEBHOOK_HOST` с HTTPS доменом

## 🔄 Webhook настройка

При запуске с `WEBHOOK_HOST` бот автоматически:

* Удаляет старый вебхук
* Устанавливает новый вебхук
* Логирует статус вебхука
* Отслеживает количество ожидающих обновлений

## 🤝 Разработка
### Добавление новых команд

* Создайте роутер в `handlers/bot_routes/`
* Импортируйте и зарегистрируйте в `handler_bot.py`

Пример:
```python
# handlers/bot_routes/custom_routes.py
from aiogram import Router, types
from aiogram.filters import Command

custom_router = Router()

@custom_router.message(Command("custom"))
async def custom_handler(message: types.Message):
    await message.answer("Custom command!")
```

Затем в `handler_bot.py`:

```python
from handlers.bot_routes.custom_routes import custom_router

dispatcher.include_router(custom_router)
```

### Добавление API эндпоинтов

* Создайте роутер в `routes/`
* Импортируйте и зарегистрируйте в `core.py`

Пример:
```python
# routes/custom_api.py
from fastapi import APIRouter

custom_api_router = APIRouter(tags=["custom"])

@custom_api_router.get("/api/custom")
async def custom_endpoint():
    return {"message": "Custom API endpoint"}
```

Затем в `core.py`:
```python
from routes.custom_api import custom_api_router

application.include_router(custom_api_router)
```

## 📄 Лицензия

Этот проект распространяется под лицензией GPL-3.0. Это означает:

- ✅ Вы можете свободно использовать, изучать и модифицировать код
- ✅ Вы должны указывать авторство оригинального проекта
- ✅ Вы должны сохранять эту же лицензию в производных работах
- ❌ Вы не можете распространять производные работы под закрытой лицензией

Полный текст лицензии: [LICENSE](LICENSE)
