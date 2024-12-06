import logging
import os
import datetime
import errno

from src.utils.utils import get_workdir


class Logging:
    """
    #### how to use
    #### create logger instance
    logger = Logging("defined_logger_name").get_logger()

    #### INFO level
    logger.info(
        "any message %s",
        c
    )

    #### ERROR level
    logger.error(
        "any messge %s",
        c
    )
    """
    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)
        self.logFormatter = logging.Formatter(
            "%(asctime)s [%(levelname)-5.5s] [%(name)s] %(message)s"
        )

    def get_logger(self):
        self.logger.setLevel(logging.DEBUG)

        self.get_stream_handler()
        self.get_file_handler()

        return self.logger

    def get_stream_handler(self) -> None:
        """
        로그 표준 출력 핸들러 추가
        """
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self.logFormatter)
        self.logger.addHandler(handler)

    def get_file_handler(self) -> None:
        """
        로그 파일 출력 핸들러 추가
        """
        logPath = f"{get_workdir()}/logs"
        fileName = datetime.datetime.today().strftime('%Y-%m-%d-%H%M')
        self._make_dir_(logPath)
        handler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self.logFormatter)
        self.logger.addHandler(handler)

    @staticmethod
    def _make_dir_(path: str):
        try:
            os.makedirs(path, exist_ok=True)  
        except TypeError:
            try:
                os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise