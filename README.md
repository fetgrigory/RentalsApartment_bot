# RentalsApartment_bot
Данный бот представляет собой Telegram-бота, который помогает пользователям арендовать квартиры. Бот имеет две основные функции: администраторская панель и панель пользователя.<br />

## Бизнес-ценность бота
Внедрение бота сокращает операционные затраты и увеличивает конверсию бронирований:

| Параметр                     | Без бота               | С ботом                | Экономия/Прибыль       |
|------------------------------|------------------------|------------------------|------------------------|
| Зарплата менеджеров          | 60 000 руб./мес.       | 0 руб./мес.            | **+60 000 руб./мес.**  |
| Потери от ошибок             | 30 000 руб./мес.       | 0 руб./мес.            | **+30 000 руб./мес.**  |
| Конверсия бронирований       | 40%                    | 90%                    | **+125%**              |
| Круглосуточные заявки        | —                      | +15 бронирований/мес.  | **+45 000 руб./мес.*** |
| **Итого за год**             | —                      | —                      | **1 620 000 руб.**     |

> *Расчёты для среднего чека 3 000 руб./бронирование.

**Как считаем:**
- **Менеджер**: 1 сотрудник в Москве = 60К/мес.
- **Ошибки**: 5% от 10 бронирований/день × 3 000 руб. = 30К/мес.
- **Конверсия**: Встроенная оплата увеличивает завершённые сделки с 40% до 90%.
- **24/7**: Ночные заявки = +15 бронирований/мес. × 3 000 руб.

## Администраторская панель:
![Снимок экрана админ-панели](https://github.com/user-attachments/assets/2b35828b-cf0a-4a5c-b80f-a779f415db83)<br />
## Администраторская панель:
![Снимок экрана 2025-01-28 135058](https://github.com/user-attachments/assets/2b35828b-cf0a-4a5c-b80f-a779f415db83)<br />
![Снимок экрана 2025-01-28 135607](https://github.com/user-attachments/assets/008934e7-f866-4451-bf93-e2dfa87b173f)<br />
![Снимок экрана 2025-01-28 140221](https://github.com/user-attachments/assets/c055d313-841f-4acf-93cf-b9e206807f94)<br />
![Снимок экрана 2025-01-28 140650](https://github.com/user-attachments/assets/a6cb4cb2-a280-4859-89b7-bbd24c121437)<br />
![Снимок экрана 2025-01-28 140726](https://github.com/user-attachments/assets/441b2945-240a-4cce-8f8a-8ca351c81622)<br />
- При входе в админ-панель администратору отображается возможность добавления данных.
- Администратор может загружать фотографии квартир, вводить описания, адрес и цену. А также редактировать и удалять текущие записи в каталоге.
- Данные о квартирах сохраняются в базе данных PostgreSQL, что обеспечивает надежность, масштабируемость и высокую производительность.

## Преимущества PostgreSQL для Telegram-бота:
- **Масштабируемость и производительность**: PostgreSQL эффективно работает с большими объемами данных и множеством одновременных подключений.
- **Безопасность**: Гибкая система управления доступом и встроенные механизмы защиты данных.
- **Надежность**: Поддержка транзакций, репликации и резервного копирования.
- **Расширенные функции**: Поддержка сложных запросов, полнотекстового поиска и геоданных.
 ## Пользовательская панель:
![1](https://github.com/user-attachments/assets/1b289697-0949-4ca2-9b7b-e09d968fd17c)<br />
![Снимок экрана 2025-01-28 130904](https://github.com/user-attachments/assets/56b35dfb-efe7-4867-aa7a-ff19832cf2aa)<br />
![Снимок экрана 2025-01-28 131330](https://github.com/user-attachments/assets/8335b039-acc9-4570-b04d-35c80486fd98)<br />
![Снимок экрана 2025-01-28 132101](https://github.com/user-attachments/assets/f96e7dec-cd54-467d-b166-e88177aee595)<br />

- В каталоге квартир вы сможете просматривать доступные квартиры, просматривать фотографии, описание и цены квартир, а также оплачивать аренду фотографий через инлайн-оплату.
- Вы можете использовать кнопки "◀ Пред.", "След. ▶" для просмотра предыдущей и следующей квартиры соответственно, а также "💳Оплатить" для оплаты аренды.
- Также есть возможность зайти на 🌐 сайт компании или получить телефон ☎️

## Система оплаты PayMaster
- В боте реализована интеграция с платежной системой PayMaster для удобной и безопасной оплаты  
- **+50% к конверсии**: Встроенные платежи в Telegram увеличивают завершение бронирований на 50% по сравнению с традиционными звонками менеджеру  
![Оплата через PayMaster](https://github.com/user-attachments/assets/a1bb13ea-8507-4279-bb67-a746d8241c31)<br />
*Пример: клиент бронирует квартиру за 2 клика без ожидания ответа оператора*

### Процесс оплаты:
1. Нажмите "💳Оплатить" →  
   ![Выбор квартиры](https://github.com/user-attachments/assets/e9096683-7dd6-4ec5-87f8-ea8466ee8c32)<br />
2. Введите тестовые данные:  
   - Карта: `4100 0000 0000 0001`  
   - Срок: `03/26`  
   - CVC: `111`  
3. Получите подтверждение:  
   ![Успешная оплата](https://github.com/user-attachments/assets/0d80a590-3fff-445c-b75e-57cb32121e0f)<br />

## Система оплаты Сбербанк Test
- Поддержка бонусов СПАСИБО → дополнительное увеличение конверсии на 15-20%  
![Оплата через Сбербанк](https://github.com/user-attachments/assets/20850011-884a-449c-8d39-ee02ee141f5f)<br />
*Клиенты могут использовать накопленные баллы*

### Тестовые реквизиты:
Детали в файле [тестовые_банковские_карты.pdf]()
## Инструкция по использованию бота:<br />

Для успешного запуска и использования бота, выполните следующие шаги:

### Шаг 1: Заполнение файла ".env"
Файл ".env" содержит все важные параметры конфигурации, которые необходимы для работы бота. Убедитесь, что вы заполнили все требуемые поля:

- **TOKEN**: Токен вашего бота, который можно получить, обратившись к [@BotFather](https://t.me/BotFather).
- **ADMIN_ID**: Ваш личный ID в Telegram. Получить его можно с помощью бота [@getmyid_bot](https://t.me/getmyid_bot).
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
HOST="127.0.0.1"
DBNAME="example_db"
USER="admin_user"
PASSWORD="strongpassword"
PORT="5432"
```

### Шаг 3: Подготовка виртуального окружения и запуск бота

1. Создайте виртуальное окружение для изоляции зависимостей проекта. 
   Используйте команду:
   ```bash
   python -m venv venv
   ```

2. Активируйте виртуальное окружение:
   - На Windows:
     ```bash
     venv\Scripts\activate
     ```
   - На macOS и Linux:
     ```bash
     source venv/bin/activate
     ```
3. Запустите бота командой:
   ```bash
   python main.py
   ```

Теперь бот должен быть готов к использованию. Убедитесь, что ваше соединение с интернетом активно и все конфигурации настроены корректно. Если возникнут ошибки, проверьте файл ".env" на наличие опечаток или некорректных значений.
## Применяемые библиотеки и версия языка <br />
aiogram            3.13.1 <br />
python-dotenv      1.0.1 <br />
psycopg2  2.9.10 <br />
python 3.11.9 <br />
