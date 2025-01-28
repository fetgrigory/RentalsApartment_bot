# RentalsApartment_bot
Данный бот представляет собой Telegram-бота, который помогает пользователям арендовать квартиры. Бот имеет две основные функции: администраторская панель и панель пользователя. <br />
## Администраторская панель:
![0](https://github.com/fetgrigory/RentalsApartment_bot/assets/157891679/152adcd0-49fb-48c3-9ffe-b4f9b43a56b3)<br />
![143714](https://github.com/user-attachments/assets/e64046bb-48bb-4931-a3ce-2dec01f6c7ed)<br />
![144855](https://github.com/user-attachments/assets/459005a5-e61f-4d2a-bd00-4a26b99b8cf3)<br />
![145221](https://github.com/user-attachments/assets/a8e084a6-97b7-4590-8b38-fa1c5b18f31e)<br />
- При входе в админ-панель администратору отображается возможность добавления данных.
- Администратор может загружать фотографии квартир, вводить описания, адрес и цену. А также редактировать и удалять текущие записи в каталоге. 
- Данные о квартирах сохраняются в базе данных SQLite, однако предусмотрена возможность альтернативного подключения к PostgreSQL, что может обеспечить более широкий функционал и производительность.
## Использование SQLite и PostgreSQL в Telegram-боте
В Telegram-боте для аренды квартир используются два типа баз данных — SQLite и PostgreSQL — позволяет гибко адаптироваться к различным требованиям разработки и эксплуатации. 

**SQLite** идеально подходит для начального этапа разработки и тестирования. Это локальная встраиваемая база данных, которая хранит все данные в одном файле, что позволяет быстро настроить и запустить приложение без необходимости сложной конфигурации серверной среды. Такая компактность и легкость делают SQLite удобной для небольших проектов или для ситуаций, где нужно минимизировать усилия на установку и управление данными.

**PostgreSQL** предоставляет важные преимущества для более сложных и растущих проектов. Она поддерживает работу с большими объемами данных и высокие нагрузки, критически важные для приложения с увеличивающимся числом пользователей и запросов. Архитектура клиента-сервера позволяет PostgreSQL эффективно обслуживать множество одновременных подключений, обеспечивая параллелизм и быстрый отклик. 

**Преимущества PostgreSQL перед SQLite для Telegram-бота:**

- **Масштабируемость и производительность**: PostgreSQL обеспечивает лучшую производительность в многопользовательских средах и с большими объемами данных, что делает её идеальной для расширения и поддержки новых функциональных возможностей бота.
- **Безопасность и управление доступом**: Автоматизированное управление пользователями и правами доступа PostgreSQL повышает безопасность, позволяя администраторам гибко настраивать доступ к данным пользователей и квартир.
- **Надежность и резервирование**: Функции репликации и резервного копирования данных в PostgreSQL обеспечивают устойчивость к сбоям, минимизируя простой и обеспечивая доступность системы.

Таким образом, использование обеих систем баз данных — SQLite для быстрого и простого старта разработки, и PostgreSQL для масштабируемого и надежного развертывания — позволяет обеспечить максимальную гибкость и надежность всей системы. Это делает бота более адаптируемым к изменяющимся требованиям и способствует более эффективному взаимодействию как с пользователями, так и с администраторами.

 ## Пользовательская панель:
![1](https://github.com/user-attachments/assets/1b289697-0949-4ca2-9b7b-e09d968fd17c)<br />
- В каталоге квартир вы сможете просматривать доступные квартиры, просматривать фотографии, описание и цены квартир, а также оплачивать аренду фотографий через инлайн-оплату.
- Вы можете использовать кнопки "◀ Пред.", "След. ▶" для просмотра предыдущей и следующей квартиры соответственно, а также "💳Оплатить" для оплаты аренды.
- Также есть возможность зайти на 🌐 сайт компании или получить телефон ☎️

 ## Система оплаты PayMaster:
- В боте реализована интеграция с платежной системой PayMaster для удобной и безопасной оплаты аренды квартиры.
- Пользователи могут нажать на кнопку "💳Оплатить" у выбранной квартиры, чтобы произвести оплату.
- После нажатия на кнопку, пользователь будет перенаправлен на страницу оплаты в системе PayMaster, где можно будет выбрать удобный способ оплаты и завершить транзакцию. 
![7](https://github.com/fetgrigory/ApartmentRentals_bot/assets/157891679/a1c60b44-db03-4990-b67a-74887f83fe5b) <br />
- Далее необходимо ввести тестовые карточные данные для оплаты:<br />
Номер карты: 4100 0000 0000 0001 <br />
MM/YY: 03/26 <br />
CVC/CVV-код: 111 <br />
![153738](https://github.com/user-attachments/assets/4ea850b0-be71-4e8f-bc61-a04f39c0c983)<br />
После чего придет сообщение от бота о успешной оплате
![155559](https://github.com/user-attachments/assets/ad2c8b18-3825-44ae-b8cc-a6f8f83db81f)

Таким образом, данный бот позволяет комфортно и удобно искать и арендовать квартиры, а система оплаты PayMaster обеспечивает безопасные и удобные платежные операции.
## Система оплаты Сбербанк Test:
 В боте реализована интеграция с платежной системой Сбербанк Test для удобной и безопасной оплаты аренды квартиры.
- Пользователи могут нажать на кнопку "💳Оплатить" у выбранной квартиры, чтобы произвести оплату.
- После нажатия на кнопку, пользователь будет перенаправлен на страницу оплаты в системе Сбербанк Test, где можно будет выбрать удобный способ оплаты и завершить транзакцию.
![Сбер1](https://github.com/user-attachments/assets/807de715-fe47-47d2-a579-dccf2f08d08d)<br />
![Сбер2](https://github.com/user-attachments/assets/97dedc27-f6bb-4065-83a3-2c30c5d65ee8)<br />
- Дополнительно, пользователи имеют возможность оплачивать аренду, используя бонусы СПАСИБО. Это позволяет снизить стоимость платежа за счет накопленных бонусов, делая оплату еще более выгодной.
Реквизиты тестовых банковских карт для Сбербанка находятся в файле "тестовые_банковские_карты.pdf"

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
sqlite3 <br />
psycopg2  2.9.10 <br />
python 3.11.9 <br />
