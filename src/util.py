"""
Utility functions for the application.
"""
import datetime


def get_timestamp():
    """Returns the current timestamp in milliseconds."""
    now = datetime.datetime.now()
    return int(now.timestamp() * 1000)
