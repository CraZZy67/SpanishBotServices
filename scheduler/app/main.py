import asyncio

from scheduler_ import Scheduler


asyncio.run(Scheduler.start(), debug=True)