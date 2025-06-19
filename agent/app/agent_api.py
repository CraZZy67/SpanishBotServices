from relevanceai import RelevanceAI

import os
import pycountry
import time

from logger import main_logger


class Agent:
    client = RelevanceAI(
        api_key=os.getenv('RAI_API_KEY'), 
        region=os.getenv('RAI_REGION'), 
        project=os.getenv('RAI_PROJEC')
    )

    agent = client.agents.retrieve_agent(os.getenv('AGENT_ID'))

    @staticmethod
    def get_prompt() -> str:
        with open('prompt.txt', 'r', encoding='utf-8') as file:
            return ''.join(file.readlines())
    
    @staticmethod
    def alpha_to_name(alpha_format: str, pycountry_list: list):
        return pycountry_list.get(alpha_2=alpha_format)

    @classmethod
    def generate_post(cls, format: str, level: int, counries: str, language: str) -> str:
        language = cls.alpha_to_name(language, pycountry.languages)
        counries = [cls.alpha_to_name(x, pycountry.countries) for x in counries.split(',')]

        level = 'A1-A2' if level else 'B1-C2'

        message = cls.get_prompt().format(
            format=format, 
            level=level, 
            countries=', '.join(counries),
            language=language
            )
        
        task = cls.agent.trigger_task(message=message)
        
        while not cls.agent.get_task_output_preview(task.conversation_id):
            main_logger.info('Генерация контента...')
            time.sleep(5.0)
        
        output = cls.agent.get_task_output_preview(task.conversation_id)
        cls.agent.approve_task(task.conversation_id)

        return output