from openai import OpenAI

import os
import random

from logger import main_logger


class Agent:

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    model = 'gpt-4o-mini'

    @staticmethod
    def get_theme(format: str):
        with open(f'theme/{format.lower()}.txt', 'r', encoding='utf-8') as file:
            return random.choice(file.readlines())
    
    @staticmethod
    def get_prompt(format: str):
        with open(f'prompt/{format.lower()}.txt', 'r', encoding='utf-8') as file:
            return file.read()

    @classmethod
    def generate_post(cls, format: str, level: str, countries: str, language: str) -> dict:
        text = cls.get_prompt(format=format)

        if format == 'Grammar' or format == 'Vocabulary':
            text = text.format(
                countries=countries,
                level=level,
                language=language,
                theme=cls.get_theme(format=format)
            )
        else:
            text = text.format(
                countries=countries,
                level=level,
                language=language
            )

        response = cls.client.responses.create(model=cls.model, input=text, tools=[{"type": "web_search_preview"}])

        return {'answer': response.output_text}