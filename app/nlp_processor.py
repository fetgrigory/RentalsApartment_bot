'''
This module make
Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 17/05/2025
Ending //

'''
# Installing the necessary libraries
from transformers import pipeline
import g4f

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
    """AI is creating summary for analyze_review

    Args:
        text (str): [description]

    Returns:
        dict: [description]
    """
    result = sentiment_analyzer(text)[0]
    return {
        "label": result["label"],
        "score": result["score"]
    }


# Get response from GPT model
def ask_gpt(messages: list) -> str:
    """AI is creating summary for ask_gpt

    Args:
        messages (list): [description]

    Returns:
        str: [description]
    """
    try:
        # Add system prompt to the beginning of messages
        messages_with_system = [{"role": "system", "content": system_prompt}] + messages
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=messages_with_system,
            timeout=60
        )
        return response
    except Exception as e:
        print(f"Error getting GPT response: {e}")
        return "Извините, в данный момент я не могу ответить на ваш вопрос. Пожалуйста, попробуйте позже."
