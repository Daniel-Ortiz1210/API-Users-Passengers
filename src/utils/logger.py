import logging
from datetime import datetime

class Logger:
    """
    A singleton Logger class to handle logging with different levels.
    Attributes:
        _instance (Logger): The singleton instance of the Logger class.
        logger (logging.Logger): The logger instance used for logging messages.
    Methods:
        __new__(cls):
            Creates and returns the singleton instance of the Logger class.
        _configure():
            Configures the logger instance with a stream handler and sets the logging level to DEBUG.
        log(level, message):
            Logs a message with the specified logging level.
            Args:
                level (str): The logging level ('INFO', 'DEBUG', 'ERROR', 'WARNING').
                message (str): The message to log.
    """
    _instance = None

    def __new__(cls):
        if cls._instance == None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._configure()
        return cls._instance
    
    def _configure(self):
        self.logger = logging.getLogger('Logger')
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            self.logger.addHandler(handler)
    
    def log(self, level, message):
        timestamp = datetime.now().isoformat()
        if level == 'INFO':
            self.logger.info(f'{timestamp} [{level}] {message}')
        elif level == 'DEBUG':
            self.logger.debug(f'{timestamp} [{level}]  {message}')
        elif level == 'ERROR':
            self.logger.error(f'{timestamp} [{level}]  {message}')
        elif level == 'WARNING':
            self.logger.warning(f'{timestamp} [{level}] {message}')
        else:
            self.logger.info(f'{timestamp} [{level}] {message}')
            