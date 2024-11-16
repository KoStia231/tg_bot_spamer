import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Создание клиента
client = TelegramClient('session_name', api_id, api_hash)


async def send_messages_with_delay(chat_id, message, counts):
    for i in range(int(counts)):
        await client.send_message(chat_id, message=message)
        print(f"Сообщение {i + 1} отправлено!")
        await asyncio.sleep(1)  # Пауза в 1 секунду


async def main():
    await client.start()
    print("Вы вошли в аккаунт Telegram!")

    chat_id = input("Введите chat_id или username куда нужно отправить сообщение:\n")
    message = input("Введите сообщение:\n")

    while True:
        counts = input("Введите количество сообщений:\n")
        try:
            counts = int(counts)
            break
        except ValueError:
            print("Ошибка: введите целое число для количества сообщений.")

    await send_messages_with_delay(chat_id, message, counts)

    await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
