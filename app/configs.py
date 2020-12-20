import os
import multiprocessing

from dotenv import load_dotenv

load_dotenv()


class AppConfig:
    HOST = os.getenv("APP_HOST")
    PORT = os.getenv("APP_PORT")
    STORAGE_PATH = os.path.join(os.getcwd(), 'storage')
    LOG_PATH = os.path.join(STORAGE_PATH, 'logs')
    DEBUG = os.getenv('DEBUG') == 'true'
    ERROR_HANDLERS = ['error_stdout'] if DEBUG else ['error']
    DEFAULT_TIMEZONE = os.getenv('DEFAULT_TIMEZONE', 'Europe/Berlin')


class DBConfig:
    HOST = os.getenv("POSTGRES_HOST")
    PORT = os.getenv("POSTGRES_PORT")
    USER = os.getenv("POSTGRES_USER")
    PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DATABASE = os.getenv("POSTGRES_NAME")


#  Gunicorn configs
bind = f'{os.getenv("APP_HOST", "127.0.0.1")}:{os.getenv("APP_PORT", 8080)}'
workers = multiprocessing.cpu_count() * 2 + 1
