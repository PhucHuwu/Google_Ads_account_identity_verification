"""
Browser management module for Google Ads Verification Tool
"""

from .driver_manager import create_chrome_driver, setup_driver_window
from .verification_processor import process_account_verification
from .task_handlers import handle_task1, handle_task2, handle_task3, check_and_execute_tasks, check_task1_available, check_task2_available, check_task3_available, get_all_available_tasks, is_verification_complete

__all__ = [
    'create_chrome_driver',
    'setup_driver_window',
    'process_account_verification',
    'handle_task1',
    'handle_task2',
    'handle_task3',
    'check_and_execute_tasks',
    'check_task1_available',
    'check_task2_available',
    'check_task3_available',
    'get_all_available_tasks',
    'is_verification_complete'
]
