import asyncio
import csv
import os

import telethon
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import InputUser

from src import API_ID, API_HASH, SESSION_DIR, LIST_USERS_DIR


async def add_users_to_group():
    """Добавление пользователей в чат или мегагруппу."""
    chat_link = input("Введите ссылку на чат (с @ для публичных чатов): ").strip()

    # Загружаем список CSV файлов с пользователями
    user_files = [f for f in os.listdir(LIST_USERS_DIR) if f.endswith('.csv')]
    if not user_files:
        print("Нет доступных CSV файлов с пользователями.")
        return

    print("\nВыберите файл с пользователями:")
    for idx, file in enumerate(user_files, start=1):
        print(f"{idx}. {file}")

    try:
        choice = int(input("Выберите номер файла с пользователями:\n")) - 1
        if choice < 0 or choice >= len(user_files):
            raise ValueError("Неверный выбор файла.")
    except ValueError:
        print("Ошибка: введите корректный номер файла.")
        return

    selected_file = user_files[choice]
    file_path = os.path.join(LIST_USERS_DIR, selected_file)

    # Загружаем список пользователей из выбранного CSV файла
    users_to_add = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='/')
        next(reader)  # Пропускаем заголовок
        for row in reader:
            if row[1] != "Нет имени пользователя":
                users_to_add.append((row[1], row[0]))  # (username, id)

    if not users_to_add:
        print("В файле нет пользователей с именами.")
        return

    sessions = [f for f in os.listdir(SESSION_DIR) if f.endswith('.session')]
    if not sessions:
        print("Нет доступных сессий.")
        return

    session_idx = 0
    current_index = 0  # Индекс текущего пользователя

    while current_index < len(users_to_add):
        session_file = os.path.join(SESSION_DIR, sessions[session_idx])
        client = TelegramClient(session_file, API_ID, API_HASH)
        await client.start()
        print(f"Используется сессия: {session_file}")

        try:
            # Получаем данные чата
            entity = await client.get_entity(chat_link)

            # Определяем тип чата
            if isinstance(entity, telethon.tl.types.Chat):
                chat_type = "Обычный чат"
            elif isinstance(entity, telethon.tl.types.Channel):
                if entity.megagroup:
                    chat_type = "Мегагруппа"
                else:
                    chat_type = "Канал"
            else:
                chat_type = "Неизвестный тип"

            print(f"Чат найден: {chat_link}, Тип: {chat_type}, ID: {entity.id}")

            if chat_type == "Канал":
                print("Добавление пользователей в каналы не поддерживается.")
                return

            # Вступление в мегагруппу (если это мегагруппа)
            if chat_type == "Мегагруппа":
                try:
                    await client(JoinChannelRequest(chat_link))
                    print(f"Сессия успешно вступила в мегагруппу {chat_link}.")
                except Exception as e:
                    print(f"Не удалось вступить в мегагруппу: {e}")
                    continue

            # Добавление пользователей
            chat_id = entity.id
            while current_index < len(users_to_add):
                username, user_id = users_to_add[current_index]
                try:
                    user = await client.get_entity(username)
                    if chat_type == "Обычный чат":
                        await client(
                            AddChatUserRequest(
                                chat_id,
                                InputUser(user_id=user.id, access_hash=user.access_hash),
                                fwd_limit=10
                            )
                        )
                    elif chat_type == "Мегагруппа":
                        await client(InviteToChannelRequest(channel=chat_id, users=[user]))

                    print(f"Пользователь {username} добавлен в {chat_type}.")
                    current_index += 1
                    await asyncio.sleep(3)
                except telethon.errors.ChatWriteForbiddenError:
                    print(f"Сессия не может писать в чат {chat_link}.")
                    break
                except Exception as e:
                    print(f"Не удалось добавить пользователя {username}: {e}")
                    current_index += 1

        except telethon.errors.InviteHashExpiredError:
            print(f"Ссылка на чат {chat_link} недействительна.")
        except Exception as e:
            print(f"Ошибка при работе с сессией {session_file}: {e}")
        finally:
            await client.disconnect()

        session_idx = (session_idx + 1) % len(sessions)
        print("Пауза 10 секунд перед подключением к следующей сессии...")
        await asyncio.sleep(10)

    print("Все пользователи добавлены.")
