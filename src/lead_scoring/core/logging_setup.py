"""
logging_setup.py
----------------

Centralized logging configuration for the project

This module provides a helper function to create and configure a logger
with both file and console handlers, ensuring consistent log formatting
across notebooks, pipelines, and production scripts

Features
--------
- Supports configurable logger names
- Writes logs to both file and stdout
- Prevents duplicate handlers on repeated calls
- Uses a standardized timestamped log format
"""


## ------------------------------------------------------------------------------------ ##
import logging
from pathlib import Path
from lead_scoring.config.paths import ROOT_DIR


## ------------------------------------------------------------------------------------ ##
def get_logger(name: str, mode="w"):

    """
    Create and configure a project-wide logger

    The logger is configured with:
    - FileHandler for persistent logs
    - StreamHandler for console output
    - INFO log level
    - Consistent timestamped formatting

    Duplicate handlers are avoided when the logger is requested multiple
    times within the same Python process.

    Parameters
    ----------
    name : str
        Name of the logger.
    mode : str, default="w"
        File open mode for the log file ('w' for overwrite, 'a' for append).

    returns
    -------
    logging.Logger
        Configured logger instance.
    """

    log_dir = Path(ROOT_DIR / "logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = Path(log_dir / f'{name}.log')

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # File handler
        fh = logging.FileHandler(log_file, mode=mode)
        fh.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)
    
    logger.propagate = False

    return logger


## ------------------------------------------------------------------------------------ ##