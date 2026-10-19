"""
exception.py
------------

Custom exception handling utilities for the pipeline.

This module provides:
- A helper function to extract detailed error information including
  file name, line number, and message.
- A CustomException class that wraps Python exceptions with enriched
  context for easier debugging and logging.
"""


## --------------------------------------------------------------------------------------------------- ##
import logging


## --------------------------------------------------------------------------------------------------- ##
def error_message_details(error, error_detail):
    """
    Construct a detailed error message with file name, line number, and message.

    Parameters
    ----------
    error : Exception
        The original exception object.
    error_detail : sys
        The sys module instance (used to extract traceback information).

    Returns
    -------
    error_message: str
        A formatted error message string containing file name, line number,
        and the exception message.

    Notes
    -----
    - Logs the error message using the root logger.
    - Intended to be used internally by CustomException.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = (
        f"Error occurred in python script - {file_name}, "
        f"line number - {line_number}, "
        f"error message - {str(error)}"
    )

    logging.error(error_message)

    return error_message

## --------------------------------------------------------------------------------------------------- ##
class CustomException(Exception):
    """
    Custom exception class for enriched error reporting.

    This class extends the base Exception class to include detailed
    error context such as file name and line number. It leverages
    `error_message_details()` to construct a descriptive message
    and logs the error automatically.

    Parameters
    ----------
    error_message : str
        The original error message or exception string.
    error_detail : sys
        The sys module instance, used to extract traceback information.

    Attributes
    ----------
    error_message : str
        A detailed error message including file name, line number,
        and the original exception message.

    Methods
    -------
    __str__() -> str
        Returns the detailed error message string.
    """

    def __init__(self, error_message, error_detail):
        super().__init__(error_message)
        self.error_message = error_message_details(error=error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message


## --------------------------------------------------------------------------------------------------- ##