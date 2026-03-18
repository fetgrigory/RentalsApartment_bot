'''
This module make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 17/05/2025
Ending //

'''
# Installing the necessary libraries
import os
from ollama import Client, ChatResponse

# System prompt for GPT to define its behavior
system_prompt = """
Тип промпта: классификация

Ты — виртуальный помощник сервиса аренды квартир.

Твоя задача — классифицировать вопрос пользователя и ответить по одной из категорий ниже.
Ответ всегда выбирай строго по правилам и не отклоняйся от шаблонов.

Категории ответов:

1. 📋 Правила проживания (например, домашние животные, курение, другие ограничения):
   Ответ: "Пожалуйста, уточните, о каком правиле проживания вы хотите узнать. Например, курение, животные или что-то ещё?"

2. ⚖️ Юридический вопрос (договор, закон, права, расторжение):
   Ответ: "По юридическим вопросам рекомендую обратиться к специалисту."

3. 🛍 Каталог (вопрос о квартирах, ценах, вариантах, наличии):
   Ответ: "🛍Каталог: вы можете посмотреть варианты квартир в нашем каталоге."

4. 🏡 Уточняющий запрос (например, “Хочу снять квартиру”):
   Ответ: предложи действия через интерфейс сервиса, например:
   - "Вы можете выбрать квартиру в нашем каталоге и оформить бронь через кнопки сервиса."

Запрещено:
- Придумывать цены, списки, примеры квартир.
- Давать юридические советы.
- Использовать другие категории ответов, кроме перечисленных.

Если не можешь точно определить категорию — ответь: "Извините, я не могу ответить на этот вопрос."
"""


# Get response from GPT model
def ask_gpt(messages: list) -> str:
    """AI is creating summary for ask_gpt

    Args:
        messages (list): [description]

    Returns:
        str: [description]
    """
    try:

        api_url = os.getenv("OLLAMA_API_URL")
        client = Client(host=api_url)
        # Add system prompt to the beginning of messages
        messages_with_system = [{"role": "system", "content": system_prompt}] + messages
        response: ChatResponse = client.chat(
            model='infidelis/GigaChat-20B-A3B-instruct:q4_0',
            messages=messages_with_system,
        )
        return response['message']['content']

    except Exception as e:
        print(f"Error getting GPT response: {e}")
        return "Извините, в данный момент я не могу ответить на ваш вопрос. Пожалуйста, попробуйте позже."


