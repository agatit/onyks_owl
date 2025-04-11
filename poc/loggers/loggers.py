import logging

from rich.logging import RichHandler


class InfoLogger:
    @staticmethod
    def init(log_path):
        logger = logging.getLogger(InfoLogger.__name__)
        logger.setLevel(logging.INFO)

        # console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_path)

        # logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    @staticmethod
    def get():
        return logging.getLogger(InfoLogger.__name__)


def init_default_info_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(filename)s:%(lineno)4d - %(levelname)s - %(message)s'
    )
    return logger

def init_rich_info_logger(name: str, **config_kwargs) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.INFO,
        handlers=[RichHandler()],
        **config_kwargs
    )
    return logger
