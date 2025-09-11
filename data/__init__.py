"""
Data management module for Google Ads Verification Tool
"""

from .account_manager import load_account_data, save_account_data
from .verification_manager import load_verification_data, save_verification_data, update_verification_status
from .file_handler import browse_and_load_file

__all__ = [
    'load_account_data',
    'save_account_data',
    'load_verification_data',
    'save_verification_data',
    'update_verification_status',
    'browse_and_load_file'
]
