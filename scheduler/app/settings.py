from datetime import time

from dataclasses import dataclass


@dataclass
class Settings:
    DB_SYSTEM = 'postgresql'
    DB_DRIVER = 'psycopg2'

    CONTENT_TIME = time(hour=17, minute=10)
    POST_TIME = time(hour=17, minute=12)
    VIDEO_TIME = time(hour=17, minute=14)

    TOPICS = ['Grammar', 'Vocabulary', 'Short story']
    DIALECTS = ['Mexico', 'Spain']
    LEVELS = ['A1-A2', 'B1-C2']
    TRANSLEITS = ['Russian', 'Spanish', 'English']

    URL = 'http://agent:80/generate'
    VIDEO_URL = 'http://parser:80/get_video'