import asyncio
import os

from telethon import TelegramClient

from src import API_ID, API_HASH, SESSION_DIR


async def send_messages_with_delay(client, chat_id, message, counts):
    """Отправка сообщений с задержкой."""
    for i in range(counts):
        await client.send_message(chat_id, message=message)
        print(f"Сообщение {i + 1} отправлено!")
        await asyncio.sleep(1)  # Пауза в 1 секунду


async def send_from_single_session():
    """Отправка сообщений из выбранной сессии."""
    sessions = os.listdir(SESSION_DIR)
    if not sessions:
        print("Нет сохраненных сессий. Сначала сохраните сессию.")
        return

    print("Список доступных сессий:")
    for idx, session in enumerate(sessions, start=1):
        print(f"{idx}. {session}")

    print("0. Вернуться в главное меню")
    choice = input("Выберите сессию:\n")

    if choice == "0":
        return

    try:
        session_path = os.path.join(SESSION_DIR, sessions[int(choice) - 1])
    except (IndexError, ValueError):
        print("Неверный выбор.")
        return

    client = TelegramClient(session_path, API_ID, API_HASH)
    await client.start()

    chat_id = input("Введите chat_id или username куда нужно отправить сообщение:\n")
    message = input("Введите сообщение:\n")
    counts = int(input("Введите количество сообщений:\n"))

    await send_messages_with_delay(client, chat_id, message, counts)
    await client.disconnect()


async def send_from_all_sessions():
    """Отправка сообщений из всех сессий."""
    sessions = os.listdir(SESSION_DIR)
    if not sessions:
        print("Нет сохраненных сессий. Сначала сохраните сессию.")
        return

    chat_id = input("Введите chat_id или username куда нужно отправить сообщение:\n")
    message = input("Введите сообщение:\n")
    counts = int(input("Введите количество сообщений:\n"))

    for session in sessions:
        print(f"Использование сессии {session}")
        session_path = os.path.join(SESSION_DIR, session)
        client = TelegramClient(session_path, API_ID, API_HASH)
        await client.start()
        await send_messages_with_delay(client, chat_id, message, counts)
        await client.disconnect()
