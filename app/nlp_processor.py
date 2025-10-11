'''
This module make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 17/05/2025
Ending //

'''
# Installing the necessary libraries
import os
from transformers import pipeline
from ollama import Client, ChatResponse

# System prompt for GPT to define its behavior
system_prompt = """
Тип промпта: классификация

Ты — виртуальный помощник сервиса аренды квартир.

Твоя задача — классифицировать вопрос пользователя и ответить по одной из категорий ниже.
Ответ всегда выбирай строго по правилам и не отклоняйся от шаблонов.

Категории ответов:

1. ❌ Не по теме (вопрос не связан с арендой жилья):
   Ответ: "Извините, я могу помогать только с вопросами по аренде жилья."

2. ⚖️ Юридический вопрос (договор, закон, права, расторжение):
   Ответ: "По юридическим вопросам рекомендую обратиться к специалисту."

3. 🛍 Каталог (вопрос о квартирах, ценах, вариантах, наличии):
   Ответ: "🛍Каталог: вы можете посмотреть варианты квартир в нашем каталоге."

4. 🏡 Уточняющий запрос (например, “Хочу снять квартиру”):
   Ответ: задай 2–3 уточняющих вопроса:
     - "Какой тип жилья вы ищете?"
     - "На какой срок планируете аренду?"
     - "В каком районе предпочитаете жильё?"

Запрещено:
- Придумывать цены, списки, примеры квартир.
- Давать юридические советы.
- Использовать другие категории ответов, кроме перечисленных.

Если не можешь точно определить категорию — выбери пункт 1.
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


# Loads and returns the sentiment analysis model
def load_sentiment_model():
    """AI is creating summary for load_sentiment_model

    Returns:
        [type]: [description]
    """
    return pipeline(
        task='sentiment-analysis',
        model='blanchefort/rubert-base-cased-sentiment'
    )


# Loading the model when importing the module
sentiment_analyzer = load_sentiment_model()


# Analyzes the review text and returns the result
def analyze_review(text: str) -> dict:

    """AI is creating summary for

    Returns:
        [type]: [description]
    """
    result = sentiment_analyzer(text)[0]
    return {
        "label": result["label"],
        "score": result["score"]
    }
