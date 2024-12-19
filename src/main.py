import asyncio

from invait_def import (
    add_users_to_group
)

from save_def import (
    save_session,
    save_users_from_group
)
from spam_def import (
    send_from_single_session,
    send_from_all_sessions
)


async def main():
    while True:
        print("\nВыберите действие:")
        print("1. Сохранить новую сессию")
        print("2. Написать сообщение от одной сессии")
        print("3. Написать сообщение от всех сессий")
        print("4. Сохранить список участников группы")
        print("5. Добавить пользователей в группу")
        print("0. Выйти")

        choice = input("Введите номер действия:\n")
        if choice == "1":
            await save_session()
        elif choice == "2":
            await send_from_single_session()
        elif choice == "3":
            await send_from_all_sessions()
        elif choice == "4":
            await save_users_from_group()
        elif choice == "5":
            await add_users_to_group()
        elif choice == "0":
            print("Выход...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    asyncio.run(main())
