from typing import List, Dict
from src.nlp.llm_client import ask_gpt
from src.nlp.rag.vector_search import search_contract, format_contract_results


def process_question(message_text: str, messages: List[Dict]) -> tuple[str, List[Dict]]:
    new_messages = messages.copy()
    new_messages.append({"role": "user", "content": message_text})
    # Search contracts and respond if no results found, ask GPT
    results = search_contract(message_text, limit=3)
    if results:
        response = format_contract_results(results)
    else:
        # Get GPT's response
        response = ask_gpt(new_messages)
    new_messages.append({"role": "assistant", "content": response})
    return response, new_messages
