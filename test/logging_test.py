"""************************************************************
        File        : logging_test.py
        About       : Test logging works as expected.
        Author      : Abi Haddon
************************************************************"""


import os
import logging
import pytest
from src.logging import LoggerManager


# Instantiate the LoggerManager class
@pytest.fixture
def logger_manager():
    """Initialize a LoggerManager instance for testing purposes."""
    # Instantiate the LoggerManager class with a test log file path
    return LoggerManager('test_log.log')


def test_logger_creation(logger_manager):
    """Check if logger object is created successfully"""
    # Checking logger attribute of the LoggerManager instance is not None
    assert logger_manager.logger is not None


def test_log_levels(logger_manager, caplog):
    """Tests log messages are recorded at all levels & captured correctly"""

    # Get the logger object from LoggerManager
    logger = logger_manager.logger
    # Check if log messages are recorded at different levels
    logger.warning('Warning Message')
    logger.error('Error Message')
    logger.critical('Critical Message')

    # Check if log messages are captured in log 'caplog.txt'
    assert 'Warning Message' in caplog.text
    assert 'Error Message' in caplog.text
    assert 'Critical Message' in caplog.text


def test_log_file_creation(logger_manager):
    """Check if log file is created"""
    log_file_path = 'test_log.log'
    # checking if the file path exists using 'os.path.exists()'
    assert os.path.exists(log_file_path)


def test_log_message_format(logger_manager):
    """Ensures that log messages are formatted correctly."""

    # Check if log messages are formatted correctly
    # defines the path to the log file that we want to open and read.
    log_file_path = 'test_log.log'
    # open file in read mode. 'with' ensure file is properly closed
    with open(log_file_path, 'r') as f:
        lines = f.readlines()
        # Verify the last line of the log file for correct formatting
        last_line = lines[-1].strip()
        # Check if it starts with a timestamp
        assert last_line.startswith('24')


if __name__ == "__main__":
    pytest.main(['-vv', 'logging_test.py'])
