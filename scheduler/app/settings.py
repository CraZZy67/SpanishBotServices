from datetime import time

from dataclasses import dataclass


@dataclass
class Settings:
    DB_SYSTEM = 'postgresql'
    DB_DRIVER = 'psycopg2'

    CONTENT_TIME = time(hour=13, minute=56)
    POST_TIME = time(hour=13, minute=58)
    VIDEO_TIME = time(hour=14, minute=0)

    TOPICS = ['Grammar', 'Story', 'Vocabulary', "Quiz", "Declension"]
    DIALECTS = ['Mexico', 'Spain']
    LEVELS = ['A1-A2', 'B1-C2']
    TRANSLEITS = ['Russian', 'Spanish', 'English']

    URL = 'http://agent:80/generate'
    VIDEO_URL = 'http://parser:80/get_video'