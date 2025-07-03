import asyncio

from scheduler_ import Scheduler
from logger import  main_logger


main_logger.debug('Сервис запущен')
asyncio.run(Scheduler.start(), debug=True)