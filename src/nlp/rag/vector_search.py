"""
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 13/03/2026
Ending //
"""
from sentence_transformers import SentenceTransformer
from sqlalchemy import text, bindparam
from pgvector.sqlalchemy import Vector
from src.db.database import sync_engine

# Загружаем модель для embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')


# Search for similar objects using a text query
def search_contract(query_text: str, limit: int = 3) -> list:
    """AI is creating summary for search_contract

    Args:
        query_text (str): [description]
        limit (int, optional): [description]. Defaults to 3.

    Returns:
        list: [description]
    """
    # Generating the embedding request
    query_embedding = model.encode(query_text).tolist()

    # SQL query to the document_chunks table
    stmt = text("""
        SELECT
            text,
            1 - (embedding <=> :query) AS similarity
        FROM document_chunks
        ORDER BY embedding <=> :query
        LIMIT :limit
    """).bindparams(bindparam("query", type_=Vector(384)))

    with sync_engine.connect() as conn:
        result = conn.execute(stmt, {"query": query_embedding, "limit": limit})
        return result.fetchall()


# Formats the search results into a string for display to the user
def format_contract_results(results: list) -> str:
    """AI is creating summary for format_contract_results

    Args:
        results (list): [description]

    Returns:
        str: [description]
    """
    if not results:
        return "Информация по договору не найдена."

    lines = []
    for idx, (text_chunk, similarity) in enumerate(results, 1):
        if similarity > 0.75:
            indicator = "🟢"
        elif similarity > 0.60:
            indicator = "🟡"
        else:
            indicator = "🟠"
        lines.append(f"{indicator} {idx}. {text_chunk[:200]}...\n   Релевантность: {similarity:.1%}")

    return "\n\n".join(lines)