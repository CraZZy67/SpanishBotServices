from datetime import time

from dataclasses import dataclass


@dataclass
class Settings:
    DB_SYSTEM = 'postgresql'
    DB_DRIVER = 'psycopg2'

    CONTENT_TIME = time(hour=19, minute=20)
    POST_TIME = time(hour=19, minute=30)
    VIDEO_TIME = time(hour=5, minute=6)

    TOPICS = ['Grammar', 'Story', 'Vocabulary']
    DIALECTS = ['Mexico', 'Spain']
    LEVELS = ['A1-A2', 'B1-C2']
    TRANSLEITS = ['Russian', 'Spanish', 'English']

    URL = 'http://agent:80/generate'
    VIDEO_URL = 'http://parser:80/get_video'

    SUBSCRIBE_PECULIARITIES = {
        'Trial': {'warp': [8], 'quiz': [1], 'declension': [0], 'phrases': [0]},
        'Basic': {'warp': [8], 'quiz': [1], 'declension': [0], 'phrases': [0]},
        'Premium': {'warp': [8], 'quiz': [1, 3, 5], 'declension': [2], 'phrases': [0]},
        'Basic': {'warp': [8], 'quiz': [8], 'declension': [6, 2, 4], 'phrases': [0]}
    }
