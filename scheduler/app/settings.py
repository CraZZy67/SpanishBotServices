from datetime import datetime, time

from dataclasses import dataclass


@dataclass
class Settings:
    DB_SYSTEM = 'postgresql'
    DB_DRIVER = 'psycopg2'

    CONTENT_TIME = time(hour=1, minute=0)
    POST_TIME = time(hour=10, minute=0)

    TOPICS = ['Grammar', 'Vocabulary', 'Short story']
    DIALECTS = ['mexico', 'spain']
    LEVELS = ['A1-A2', 'B1-C2']
    TRANSLEITS = ['Russian', 'Spanish', 'English']

    URL = 'http://agent/generate'