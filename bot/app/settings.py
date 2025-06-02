from dataclasses import dataclass

import json
import os
from pathlib import PurePath
from typing import List


@dataclass
class Settings:
    LOCALE_PATH = PurePath('locale')
    LOCALE_FILE_FORMAT = '.json'
    
    FILE_ENCODING = 'utf-8'
    
    START_TEXT = 'Hello, choose your language'
    
    LOG_PATH = PurePath('log')
    
    DB_SYSTEM = 'postgresql'
    DB_DRIVER = 'psycopg2'
    
class Locale:
    
    @classmethod
    def get_locales(cls):
        list_files = os.listdir(Settings.LOCALE_PATH)
        locales = list()
        
        for file in list_files:
            if Settings.LOCALE_FILE_FORMAT in file:
                locales.append(file.split('.')[0])
        
        cls.locales: List[str] = locales 
        
    @classmethod
    def get_locale_text(cls, locale_name: str) -> dict:
        for locale in cls.locales:
            if locale_name in locale:
                locale_file_path = PurePath(Settings.LOCALE_PATH, locale_name + Settings.LOCALE_FILE_FORMAT)
                
                with open(locale_file_path, 'r', encoding=Settings.FILE_ENCODING) as file:
                    return json.loads(file.read())
        
        

