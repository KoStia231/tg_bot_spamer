import os
from telethon import TelegramClient
from src import API_ID, API_HASH, SESSION_DIR


async def save_session():
    """Сохранение новой сессии с номером телефона."""
    phone = input("Введите номер телефона (с кодом страны):\n")
    session_path = os.path.join(SESSION_DIR, f"{phone}.session")
    client = TelegramClient(session_path, API_ID, API_HASH)

    await client.start(phone=phone)
    print(f"Сессия для {phone} успешно сохранена!")
    await client.disconnect()

