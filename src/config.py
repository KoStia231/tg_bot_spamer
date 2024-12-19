import os

from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
# директория хранения сессий
SESSION_DIR = "src/sessions"
os.makedirs(SESSION_DIR, exist_ok=True)
# сессия которая парсит список участников чата
SESSION_ADMIN_NAME = os.getenv('SESSION_ADMIN_NAME')
SESSION_FILE_ADMIN = os.path.join(SESSION_DIR, SESSION_ADMIN_NAME)
# директория хранения списков пользователей
LIST_USERS_DIR = "src/list_users"
os.makedirs(LIST_USERS_DIR, exist_ok=True)
