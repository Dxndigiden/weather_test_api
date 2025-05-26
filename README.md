# 🌤️ Weather Forecast App

Приложение на FastAPI для получения прогноза погоды по городам с HTML-интерфейсом, автодополнением, сохранением истории запросов и отображением топа популярных городов.

---

## 📦 Возможности

- 🔍 Поиск прогноза по городу на **сегодня или завтра**
- ⌨️ **Автодополнение** при вводе названия города
- 📊 Статистика самых популярных городов
- 🍪 Сохранение последнего введённого города в Cookie
- 🌐 HTML-интерфейс с Bootstrap, HTMX и Chart.js
- 📁 API-эндпоинты для данных в JSON
- 🐳 Поддержка Docker + облачный сервер Selectel 
- 🧪 Покрытие тестами через `pytest`


Update: Также приложение доступно в [интернете](http://87.228.96.69/)
---

## 🚀 Локальный запуск

### 1. Клонируй репозиторий

```bash
git clone https://github.com/Dxndigiden/weather_test_api.git
cd weather_test_api
```

### 2. Установи зависимостей

```bash
python -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Примени миграции

```bash
alembic upgrade head
```

### 4. Запусти приложение

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
Swagger-документация: [http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger)

---

## 🐳 Запуск через Docker

### 1. Собери контейнер

```bash
docker compose build
```

### 2. Запусти контейнер

```bash
docker compose up
```

Приложение будет доступно по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Запуск тестов

```bash
pytest
```

Либо в Docker:

```bash
docker compose run web pytest
```

---

## 📂 API и маршруты

### 🔸 `GET /`

Показывает HTML-форму для ввода города и выбора дня.

---

### 🔸 `POST /`

Получает прогноз по указанному городу и дню (сегодня/завтра), сохраняет в БД, возвращает результат на HTML-странице.

**Параметры формы:**

- `city`: название города (обязательно)
- `day`: `today` или `tomorrow`

---

### 🔸 `GET /autocomplete?q=...`

Возвращает список подсказок по введённой строке (минимум 2 символа).

**Пример:** `/autocomplete?q=mos`

```json
["Moscow", "Mostar", "Mosul"]
```

---

### 🔸 `GET /top`

HTML-страница с таблицей самых популярных городов по запросам.

---

### 🔸 `GET /api/v1/top`

JSON API с топом самых популярных городов.

**Ответ:**

```json
[
  { "city": "Moscow", "count": 15 },
  { "city": "Berlin", "count": 9 }
]
```

---

## 📁 Структура проекта

```
app/
├── main.py              # Мейн файл
├── api/                 # Роутеры
├── crud/                # CRUD-функции (SQLAlchemy 2.0)
├── db/                  # ДБ
├── models/              # SQLAlchemy-модели
├── schemas/             # Pydantic-схемы
├── services/            # Запрос данных погоды
├── templates/           # Html шаблоны
├── static/              # Красота (В дальнейшем)
tests/                   # Pytest-тесты (Пока мало покрытия)
alembic/                 # Миграции
```

---

## 🧾 Автор

Автор: [Dxndigiden](https://github.com/Dxndigiden)