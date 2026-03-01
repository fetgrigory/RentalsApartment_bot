'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 25/02/2026
Ending //

'''
# Installing the necessary libraries
from sentence_transformers import SentenceTransformer
from sqlalchemy import text, bindparam
from pgvector.sqlalchemy import Vector
from src.db.database import sync_engine

model = SentenceTransformer('all-MiniLM-L6-v2')


# Search for similar objects using text query
def search_catalog(query_text: str, limit: int = 1) -> list:
    # Converts text into semantic vector for search
    query_embedding = model.encode(query_text).tolist()
    with sync_engine.connect() as conn:
        # SQL query to find similar objects using vector similarity
        stmt = text("""
            SELECT
                description,
                address,
                category,
                1 - (embedding <=> :query) AS similarity
            FROM catalog
            ORDER BY embedding <=> :query
            LIMIT :limit
        """).bindparams(bindparam("query", type_=Vector(384)))

        result = conn.execute(stmt, {"query": query_embedding, "limit": limit})
        return result.fetchall()


# Formats the search results into a string for display to the user
def format_results(results: list) -> str:
    if not results:
        return "Объекты не найдены."

    lines = []
    for idx, (description, address, category, similarity) in enumerate(results, 1):
        # indicator based on similarity
        if similarity > 0.75:
            indicator = "🟢"
        elif similarity > 0.60:
            indicator = "🟡"
        else:
            indicator = "🟠"

        lines.append(
            f"{indicator} {idx}. {description[:80]}...\n"
            f"   Адрес: {address}\n"
            f"   Категория: {category}\n"
            f"   Релевантность: {similarity:.1%}"
        )

    return "\n\n".join(lines)
