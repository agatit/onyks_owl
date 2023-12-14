import logging


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
