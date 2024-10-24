# RentalsApartment_bot
Данный бот представляет собой Telegram-бота, который помогает пользователям арендовать квартиры. Бот имеет две основные функции: администраторская панель и панель пользователя. <br />
## Демонстрация основных функций бота
![](https://github.com/user-attachments/assets/a1e4a367-1506-4f7c-8aac-b27c7109bdfd) <br />
## Администраторская панель:
![0](https://github.com/fetgrigory/RentalsApartment_bot/assets/157891679/152adcd0-49fb-48c3-9ffe-b4f9b43a56b3)<br />
![202534](https://github.com/user-attachments/assets/3b65fe88-6dc5-4925-a753-3972341ec81b)<br />

- При входе в админ-панель администратору отображается возможность добавления данных.
- Администратор может загружать фотографии квартир, вводить описания и цены.
- Данные о квартирах сохраняются в базе данных SQLite.
 ## Пользовательская панель:
 ![1](https://github.com/user-attachments/assets/27c667e3-a5f7-41e4-8228-d12cb6f3431b)<br />
![3](https://github.com/user-attachments/assets/d11d5559-ae94-440c-b53e-0c839ec7e46d)

- В каталоге квартир вы сможете просматривать доступные квартиры, просматривать фотографии, описание и цены квартир, а также оплачивать аренду фотографий через инлайн-оплату.
- Вы можете использовать кнопки "◀ Пред.", "След. ▶" для просмотра предыдущей и следующей квартиры соответственно, а также "💳Оплатить" для оплаты аренды.
- Также есть возможность зайти на 🌐 сайт компании или получить телефон ☎️
![2](https://github.com/user-attachments/assets/aca64b4f-4a75-409c-a6b6-e620a9af89eb)<br />
![4](https://github.com/user-attachments/assets/2dc76953-0f50-4f75-b206-08aa39cd3891)<br />

 ## Система оплаты PayMaster:
- В боте реализована интеграция с платежной системой PayMaster для удобной и безопасной оплаты аренды квартиры.
- Пользователи могут нажать на кнопку "💳Оплатить" у выбранной квартиры, чтобы произвести оплату.
- После нажатия на кнопку, пользователь будет перенаправлен на страницу оплаты в системе PayMaster, где можно будет выбрать удобный способ оплаты и завершить транзакцию. 
 ![5](https://github.com/user-attachments/assets/a0c913d6-dad8-4397-99bf-9cf5679c2729)<br />
- Далее необходимо ввести тестовые карточные данные для оплаты:<br />
Номер карты: 4100 0000 0000 0001 <br />
MM/YY: 03/26 <br />
CVC/CVV-код: 111 <br />
![7](https://github.com/fetgrigory/ApartmentRentals_bot/assets/157891679/a1c60b44-db03-4990-b67a-74887f83fe5b) <br />

После чего придет сообщение от бота о успешной оплате
![Снимок экрана 2024-10-07 203048](https://github.com/user-attachments/assets/ab8b2a67-5deb-4fbb-bf48-5979862ac14e)<br />
Таким образом, данный бот позволяет комфортно и удобно искать и арендовать квартиры, а система оплаты PayMaster обеспечивает безопасные и удобные платежные операции.
## Инструкция по использованию бота:<br />
1. Необходимо заполнить значения в файле ".env" <br />
Пример заполнения:<br />
TOKEN=5771881671:AAFMRQNCMz6C73-NrI0f0i9kfOC-eHvvkAo<br />
ADMIN_ID=5525270361<br />
PAYMENTS_TOKEN=5771881671:AAFMRQNCMz6C73-NrI0f0i9kfOC-eHvvkAo<br />
Для получения TOKEN и PAYMENTS_TOKEN нужно вызвать бота [@BotFather](https://t.me/BotFather) <br />
Для получения ADMIN_ID нужно вызвать бота [@getmyid_bot](https://t.me/getmyid_bot) <br />
3. Запустите бота при помощи команнды "python main.py" <br />
## Применяемые библиотеки:<br />
aiogram            2.14.3 <br />
python-dotenv  1.0.1 <br />
sqlite3 <br />
