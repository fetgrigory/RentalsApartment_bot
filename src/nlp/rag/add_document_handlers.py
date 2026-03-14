'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 14/03/2026
Ending //

'''
# Installing the necessary libraries
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from src.states import AddDocumentState
from sentence_transformers import SentenceTransformer
from src.db.crud import insert_contract_data

# Model for creating embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
router = Router()


# Adding an documents
@router.message(F.text == "➕Добавить документ")
async def add_document_handler(message: types.Message, state: FSMContext):
    await state.set_state(AddDocumentState.TEXT)
    await message.answer("Введите текст документа:")


@router.message(AddDocumentState.TEXT)
async def handle_document_text(message: types.Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer("⚠ Пожалуйста, введите имено текст!")
        return
    text = message.text
    embedding_vector = embedding_model.encode(text, convert_to_numpy=True).tolist()

    insert_contract_data({
        "text": text,
        "embedding": embedding_vector
    })

    await state.clear()
    await message.answer("✅ Документ успешно добавлен!")
