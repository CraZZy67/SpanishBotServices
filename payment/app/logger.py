import logging

from settings import Settings


main_logger = logging.getLogger(__name__)
handler = logging.FileHandler(Settings.LOG_PATH, encoding=Settings.FILE_ENCODING)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]')

handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

main_logger.addHandler(stream_handler)
main_logger.addHandler(handler)
main_logger.setLevel(logging.DEBUG)