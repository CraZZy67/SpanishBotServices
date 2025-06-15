from dataclasses import dataclass

from pathlib import  PurePath


@dataclass
class Settings:
    DB_SYSTEM = 'postgresql'
    DB_DRIVER = 'psycopg2'

    FILE_ENCODING = 'utf-8'
    LOG_PATH = PurePath('log', 'logs.log')