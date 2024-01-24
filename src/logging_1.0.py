"""*********************************************************
File   :Logging_1.0.py
About  :Script for logging progress and problems within app
Author : Abi Haddon
************************************************************"""

import logging
import sys
from logging.handlers import RotatingFileHandler


class LoggerManager:
    """
    The LoggerManager class for the simple configuration
    of a logging system with a rotating file handler and a
    stream handler.

    Attributes:
        logger (logging.logger): The logger object for recording
        log messages.
    """

    def __init__(self, log_file_path='your_log_file.log'):
        """
        Initializes the LoggerManager with the specified log file path.

        Parameters:
            log_file_path (str): The path to the log file.
        """
        try:
            # Create a logger with the name of the current module
            self.logger = logging.getLogger(__name__)
            # Set the logger level to DEBUG
            self.logger.setLevel(logging.DEBUG)

            # Define a formatter with the desired log message format
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(module)s - '
                                          '%(levelname)s - %(message)s - %(lineno)d',
                                           datefmt='%y-%m-%d %H:%M:%S')

            # Create a rotating file handler for log files
            file_handler = RotatingFileHandler(log_file_path, maxBytes=20480, backupCount=5)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)

            # Create a stream handler to output log messages to the console
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(logging.DEBUG)

            # Add both handlers to the logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

            # Set up a custom exception handler for uncaught exceptions
            sys.excepthook = self.handle_exception

        except Exception as e:
            # Log initialization errors
            print(f"Error during logger initialization: {e}")
            sys.exit(1)

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        # Log uncaught exceptions with the logger
        self.logger.error("Uncaught exception",
                          exc_info=(exc_type, exc_value, exc_traceback))
        """
        Custom exception handler to log uncaught exceptions.

        Parameters:
            exc_type: Type of exception.
            exc_value: Value associated with the exception.
            exc_traceback: Traceback information for the exception.
        """

# Example usage
if __name__ == "__main__":
    # Create an instance of the LoggerManager class
    logger_manager = LoggerManager()

    try:
        # Log some messages at different levels
        logger_manager.logger.debug('This is a debug message.')
        logger_manager.logger.info('This is an info message.')
        logger_manager.logger.warning('This is a warning message.')
        logger_manager.logger.error('This is an error message.')
        logger_manager.logger.critical('This is a critical message.')
    except Exception as e:
        # Log exceptions that may occur during execution
        logger_manager.logger.error(f"An exception occurred during "
                                    f"execution: {e}")