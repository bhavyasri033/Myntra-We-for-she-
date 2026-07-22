"""
Logger Utility Module for ml_intelligence
Provides clean standard logging across the ML Intelligence service.
"""

import logging
from typing import Optional


def get_logger(name: str = "ml_intelligence") -> logging.Logger:
    """Returns a configured standard logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
