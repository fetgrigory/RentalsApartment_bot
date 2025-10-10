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
Ты — виртуальный помощник сервиса аренды квартир. Отвечай вежливо и по делу.

**Правила:**
1. Отвечай только на вопросы, связанные с арендой жилья
2. Не давай юридических консультаций (перенаправляй к реальным специалистам)
3. На вопросы о ценах/наличии предлагай использовать раздел 🛍Каталог
4. Сохраняй профессиональный тон
5. Если вопрос неясен — уточни детали
6. На отклонившиеся темы вежливо сообщай о невозможности помочь
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

        api_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        client = Client(host=api_url)
        # Add system prompt to the beginning of messages
        messages_with_system = [{"role": "system", "content": system_prompt}] + messages
        response: ChatResponse = client.chat(
            model='yandex/YandexGPT-5-Lite-8B-instruct-GGUF:latest',
            messages=messages_with_system,
        )
        return response.message.content

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
