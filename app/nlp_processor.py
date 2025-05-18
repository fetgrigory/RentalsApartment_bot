'''
This module make
Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 17/05/2025
Ending //

'''
# Installing the necessary libraries
from transformers import pipeline


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
