import requests

from datetime import datetime
from time import sleep

from settings import Settings
from logger import main_logger

class Provider:
    
    @classmethod
    def generate_combinations(cls, format: str):
        combinations = dict()
        added_combinations = dict()

        for dialect in Settings.DIALECTS:
            combinations.update({dialect: {}})
            for level in Settings.LEVELS:
                combinations[dialect].update({level: {}})
                for translation in Settings.TRANSLEITS:
                    data = {
                        'format': format,
                        'level': level,
                        'countries': dialect,
                        'language': translation,
                    }

                    response = requests.post(Settings.URL, json=data)
                    main_logger.debug(response.text)
                    sleep(21.0)

                    main_logger.debug(f'Warp combination generating...')

                    combinations[dialect][level].update({translation: response.json()['answer']})
        
        for added in ["Quiz", "Declension"]:
            added_combinations.update({added: {}})
            for dialect in Settings.DIALECTS:
                added_combinations.update({dialect: {}})
                for level in Settings.LEVELS:
                    added_combinations[dialect].update({level: {}})
                    for translation in Settings.TRANSLEITS:
                        data = {
                            'format': added,
                            'level': level,
                            'countries': dialect,
                            'language': translation,
                        }

                        response = requests.post(Settings.URL, json=data).json()
                        sleep(21.0)

                        main_logger.debug(f'Added combination generating...')

                        added_combinations[dialect][level].update({translation: response['answer']})

        cls.combinations = combinations, added_combinations
    
    @classmethod
    def get_text(cls, user, user_status: str):
        text_list = list()

        if datetime.isoweekday() in Settings.SUBSCRIBE_PECULIARITIES[user_status]['warp'] or 8 in Settings.SUBSCRIBE_PECULIARITIES[user_status]['warp']:
            text_list.append(cls.combinations[0][user[5]][user[4]][user[3]])
        if datetime.isoweekday() in Settings.SUBSCRIBE_PECULIARITIES[user_status]['quiz'] or 8 in Settings.SUBSCRIBE_PECULIARITIES[user_status]['quiz']:
            text_list.append(cls.combinations[1]['Quiz'][user[5]][user[4]][user[3]])
        if datetime.isoweekday() in Settings.SUBSCRIBE_PECULIARITIES[user_status]['declension'] or 8 in Settings.SUBSCRIBE_PECULIARITIES[user_status]['declension']:
            text_list.append(cls.combinations[1]['Declension'][user[5]][user[4]][user[3]])
        if datetime.isoweekday() in Settings.SUBSCRIBE_PECULIARITIES[user_status]['phrases'] or 8 in Settings.SUBSCRIBE_PECULIARITIES[user_status]['phrases']:
            text_list.append(cls.combinations[1]['Phrases'][user[5]][user[4]][user[3]])

        return text_list