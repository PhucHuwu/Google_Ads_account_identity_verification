"""
Utils module for Google Ads Verification Tool
"""

from .chrome_manager import kill_existing_chrome_drivers
from .validation import check_account_name
from .logging import log_with_timestamp

__all__ = [
    'kill_existing_chrome_drivers',
    'check_account_name',
    'log_with_timestamp'
]
