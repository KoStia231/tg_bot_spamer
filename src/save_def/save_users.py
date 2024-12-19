import csv
import os

from telethon import TelegramClient
from telethon.errors import ChatAdminRequiredError
from telethon.tl.types import Chat, Channel

from src import (
    API_ID, API_HASH,
    LIST_USERS_DIR,
    SESSION_FILE_ADMIN
)


async def save_users_from_group():
    """Сохранение списка участников выбранной группы."""
    client = TelegramClient(SESSION_FILE_ADMIN, API_ID, API_HASH)
    await client.start()

    try:
        # Получение списка диалогов (только групп, исключая каналы)
        dialogs = await client.get_dialogs()
        groups = [
            dialog for dialog in dialogs
            if isinstance(dialog.entity, Chat) or (isinstance(dialog.entity, Channel) and dialog.entity.megagroup)
        ]

        if not groups:
            print("У пользователя нет доступных групп.")
            return

        # Вывод списка групп с нумерацией
        print("\nСписок доступных групп:")
        for idx, group in enumerate(groups, start=1):
            print(f"{idx}. {group.name}")

        print("0. Вернуться в главное меню")
        choice = input("Выберите номер группы:\n")

        if choice == "0":
            return

        try:
            group_index = int(choice) - 1
            if group_index < 0 or group_index >= len(groups):
                raise ValueError("Неверный выбор группы.")
        except ValueError:
            print("Ошибка: введите корректный номер группы.")
            return

        selected_group = groups[group_index]
        group_name = selected_group.name.replace(" ", "_").replace("/", "_")
        file_path = os.path.join(LIST_USERS_DIR, f"{group_name}.csv")

        # Парсинг участников
        print(f"Получение списка участников группы: {selected_group.name}")
        participants = await client.get_participants(selected_group)

        # Сохранение участников в CSV
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter='/')
            writer.writerow(["ID", "Имя пользователя", "Телефон"])  # Заголовки
            for user in participants:
                username = user.username or "Нет имени пользователя"
                phone = user.phone or "Нет телефона"
                writer.writerow([user.id, username, phone])

        print(f"Список участников группы '{selected_group.name}' сохранен в файл {file_path}.")

    except ChatAdminRequiredError:
        print("Ошибка: недостаточно прав для просмотра участников группы.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        await client.disconnect()
