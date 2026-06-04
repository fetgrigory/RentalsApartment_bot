# 🏠 RentalsApartment_bot  

Telegram-бот для управления объектами недвижимости, бронирования и обработки пользовательских запросов.

Проект реализует полный цикл работы с данными: от ввода и хранения до бронирования и оплаты.


## 🚀 Основная функциональность

### 👤 Пользователь
- просмотр каталога объектов с пагинацией  
- круглосуточное бронирование с проверкой конфликтов дат  
- оплата через Telegram  
- отправка отзывов
- Нейропомощник: отвечает на вопросы пользователей с помощью локальной LLM через платформу Ollama.

### 👨‍💻 Администратор
- добавление и редактирование объектов  
- управление каталогом  
- просмотр бронирований  
- работа с отзывами пользователей  
---
## 🏗️ Архитектура

Проект построен вокруг разделения ролей **администратора** и **пользователя**, с централизованным хранилищем данных и отдельными компонентами для управления каталогом, бронирований и автоматической классификации отзывов пользователей:
```mermaid
graph TD
    subgraph "👨‍💼 Администратор"
        A[Админ-панель] --> B[Управление каталогом]
        A --> C[Просмотр бронирований]
        A --> D[Просмотр отзывов]
        B --> PostgreSQL[(PostgreSQL)]
        C --> PostgreSQL
        D --> PostgreSQL
    end

    subgraph "👤 Пользователь"
        U[Пользователь] --> E[Каталог квартир]
        U --> F[Бронирование]
        U --> G[Отзывы]
        U --> H[Чат-помощник]
        E --> PostgreSQL
        F --> Payment[Платежная система]
        G --> PostgreSQL
        H --> NLP[NLP: RuBERT + GigaChat]
    end
```


### Аналитика отзывов с RuBERT

Бот использует модель RuBERT для анализа пользовательских отзывов  
и автоматической классификации их по тональности.

| Категория | Пример отзыва | Классификация |
|------------|---------------|----------------|
| **Позитивный** | «Отличная квартира, всё чисто и удобно!» | 😊 Positive |
| **Нейтральный** | «Жильё соответствует описанию.» | 😐 Neutral |
| **Негативный** | «Слишком шумно по ночам.» | 😠 Negative |

### Тестирование платежей
Используйте тестовые карты:
- **PayMaster**: `4100 0000 0000 0001` <br />
Срок действия: 03/26<br />
CVC/CVV: 111<br />

### Проверка админ-панели
1. Добавьте новую квартиру через "➕Добавить данные"
2. Проверьте редактирование через "✏️Редактировать каталог"
3. Убедитесь, что бронирования появляются в "📜Список бронирований"
## 📸 Скриншоты

### Админ-панель
<img width="1049" height="999" alt="Снимок экрана 2025-09-21 194522" bot="https://github.com/user-attachments/assets/73b30e1e-9657-45d8-b2f6-1423b6e938bf" /><br />
![Снимок экрана 2025-05-19 203315](https://github.com/user-attachments/assets/79582897-ae75-42a9-9500-3410c01c4786)<br />
![Снимок экрана 2025-05-19 204407](https://github.com/user-attachments/assets/fc5f0f3f-a8d7-44ab-9088-3632b4ae8691)<br />
![Снимок экрана 2025-05-19 205924](https://github.com/user-attachments/assets/2d7ba07a-87cd-4669-8d30-b06a27e5d126)<br />
![Снимок экрана 2025-05-19 212014](https://github.com/user-attachments/assets/184f5746-3452-489b-9f16-11226d07e064)<br />
![Снимок экрана 2025-05-19 222702](https://github.com/user-attachments/assets/fa6aa593-7c30-4712-8fe7-e4f4e68b3096)<br />
![Снимок экрана 2025-05-19 225710](https://github.com/user-attachments/assets/6b6b5c31-b507-4830-8334-0b9a2502da1f)<br />

### Пользовательский интерфейс
![Снимок экрана 2025-06-06 164056](https://github.com/user-attachments/assets/863e2b1a-277e-4d5c-b589-1539369ab59e)<br />
![Снимок экрана 2025-06-06 174935](https://github.com/user-attachments/assets/bcca3b84-dd47-4f76-a1c3-b8944e0e091c)<br />
![Снимок экрана 2025-06-06 170135](https://github.com/user-attachments/assets/99fa905e-e864-4dc3-86a5-50eaa15c60c3)<br />
![Снимок экрана 2025-06-06 172754](https://github.com/user-attachments/assets/65fa2593-5fc5-4f94-bb53-1b26024d326a)<br />
![Снимок экрана 2025-06-06 173428](https://github.com/user-attachments/assets/f340ae76-4c3b-49d0-a55b-7441eefeea44)<br />

## 💳 Платежные системы
### PayMaster
![Процесс оплаты](https://github.com/user-attachments/assets/a1bb13ea-8507-4279-bb67-a746d8241c31)<br />
*Преимущество: мгновенное подтверждение брони*

---
## 📂 Структура проекта

```text
RentalsApartment_bot/
├── apps/                         # Django приложения
│   ├── core/                     # Базовое приложение проекта
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   └── rooms/                     # Модуль работы с комнатами/объектами
│       ├── migrations/
│       │   └── __init__.py
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── tests.py
│       └── views.py
├── config/                       # Конфигурация проекта Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── bot/                          # Основной backend / бизнес-логика приложения
│   ├── common/                   # Общие компоненты проекта
│   │   ├── __init__.py
│   │   ├── callbacks.py
│   │   └── texts.py
│   ├── db/                       # Работа с базой данных
│   │   ├── __init__.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   └── models.py
│   ├── handlers/                 # Обработчики (API / логика взаимодействия)
│   │   ├── __init__.py
│   │   ├── catalog_handlers.py
│   │   └── user_handlers.py
│   ├── keyboards/                # Клавиатуры интерфейса
│   │   ├── __init__.py
│   │   ├── admin_keyboard.py
│   │   └── user_keyboard.py
│   ├── nlp/                      # NLP и работа с LLM
│   │   ├── rag/                 # Retrieval-Augmented Generation модуль
│   │   │   ├── __init__.py
│   │   │   ├── add_document_handlers.py
│   │   │   └── vector_search.py
│   │   ├── __init__.py
│   │   ├── llm_client.py
│   │   └── sentiment_analyzer.py
│   ├── services/                # Бизнес-сервисы приложения
│   │   ├── __init__.py
│   │   ├── ai_service.py
│   │   ├── booking_service.py
│   │   └── reservation_draft.py
│   ├── utils/                   # Вспомогательные утилиты
│   │   ├── __init__.py
│   │   ├── catalog_utils.py
│   │   └── paginator.py
│   ├── payment.py               # Логика платежей
│   └── states.py               # FSM состояния
├── .dockerignore                 # Игнор для Docker
├── .env                          # Переменные окружения
├── .gitignore                    # Игнор Git
├── .python-version              # Версия Python
├── docker-compose.yml           # Оркестрация контейнеров
├── Dockerfile                   # Сборка контейнера
├── main.py                      # Точка входа приложения
├── manage.py                    # Django CLI
├── pyproject.toml              # Конфигурация проекта и зависимостей
├── README.md                   # Документация проекта
└── uv.lock                     # Lock-файл зависимостей
```
## 🛠️ Технологии

| Модуль          | Описание                          |
|-----------------|-----------------------------------|
| `aiogram`       | Фреймворк для создания Telegram-ботов|
| `psycopg-binary`|Предкомпилированный клиент PostgreSQL для быстрого развертывания бота|
| `SQLAlchemy`| Работа с PostgreSQL через ORM и выполнение SQL-запросов|
| `pgvector`|Расширение PostgreSQL для хранения и поиска по векторным данным (эмбеддингам)|
| `python-dotenv` | Работа с переменными окружения|
| `transformers` | Библиотека для NLP и работы с трансформерами от Hugging Face|
| `sentence-transformers`|Библиотека для генерации векторных представлений текста (эмбеддингов) на основе трансформер-моделей|
| `torch` |Фреймворк PyTorch для запуска и обработки готовых нейросетевых моделей|
| `ollama`           |Локальный клиент для работы с GPT-моделями через Ollama|
| **NLP-модель**  | [blanchefort/rubert-base-cased-sentiment](https://huggingface.co/blanchefort/rubert-base-cased-sentiment) |

---
## 📦 Установка

## Инструкция по использованию бота:<br />

Для успешного запуска и использования бота, выполните следующие шаги:

### Шаг 1: Заполнение файла ".env"
Файл ".env" содержит все важные параметры конфигурации, которые необходимы для работы бота. Убедитесь, что вы заполнили все требуемые поля:

- **TOKEN**: Токен вашего бота, который можно получить, обратившись к [@BotFather](https://t.me/BotFather).
- **ADMIN_ID**: Ваш личный ID в Telegram. Получить его можно с помощью бота [@TheGetAnyID_bot](https://t.me/TheGetAnyID_bot).
- **PAYMENTS_TOKEN**: Токен для обработки платежей. Также можно получить у [@BotFather](https://t.me/BotFather).

### Пример заполнения файла .env:
```plaintext
TOKEN=ВАШ_ТОКЕН
ADMIN_ID=ВАШ_ADMIN_ID
PAYMENTS_TOKEN=ВАШ_PAYMENT_TOKEN
```
### Шаг 2: Подключение к базе данных на PostgreSQL
Для работы с базой данных требуется указать параметры подключения в файле ".env":

- **HOST**: Адрес хоста базы данных.
- **DBNAME**: Имя базы данных.
- **USER**: Имя пользователя для доступа к базе данных.
- **PASSWORD**: Пароль к базе данных.
- **PORT**: Порт для подключения (например, 5432 по умолчанию для PostgreSQL).

### Пример заполнения:
```plaintext
HOST="host.docker.internal"
DBNAME="example_db"
USER="admin_user"
PASSWORD="strongpassword"
PORT="5432"
```

### Шаг 3: Подготовка виртуального окружения и запуск бота

1. Создайте виртуальное окружение для изоляции зависимостей проекта. 
   Используйте команду:
   ```bash
   uv venv
   ```

2. Активируйте виртуальное окружение:
   - На Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - На macOS и Linux:
     ```bash
     source .venv/bin/activate
     ```
3. Установка зависимостей:
      ```bash
      uv sync
      ```
4. Запуск Ollama (скачивается образ, если нет):
   ```bash
    docker-compose up -d ollama
     ```
5. Загрузка нужной модели внутрь Ollama:
   ```bash
    docker exec -it ollama /bin/ollama pull infidelis/GigaChat-20B-A3B-instruct:q4_0
     ```
6. Проверка, что модель есть:
   ```bash
   docker exec -it ollama /bin/ollama list
     ```
7. Сборка образа в Docker:
   ```bash
    docker-compose up -d --build
     ```
8. Запуск контейнера:
   ```bash
   docker-compose up
   ```

Теперь бот должен быть готов к использованию. Убедитесь, что ваше соединение с интернетом активно и все конфигурации настроены корректно. Если возникнут ошибки, проверьте файл ".env" на наличие опечаток или некорректных значений.
