"""
UI module for Google Ads Verification Tool
"""

from .widget_creator import create_widgets, setup_window_geometry
from .tab_setup import setup_account_tab, setup_verification_tab, setup_execution_tab
from .event_handlers import setup_event_handlers, on_id_entry_focus_in, on_id_entry_focus_out, on_name_entry_focus_in, on_name_entry_focus_out, browse_file_handler
from .table_managers import update_account_table, update_verification_table, toggle_checkbox
from .status_updater import update_status_display, update_progress_display

__all__ = [
    'create_widgets',
    'setup_window_geometry',
    'setup_account_tab',
    'setup_verification_tab',
    'setup_execution_tab',
    'setup_event_handlers',
    'on_id_entry_focus_in',
    'on_id_entry_focus_out',
    'on_name_entry_focus_in',
    'on_name_entry_focus_out',
    'browse_file_handler',
    'update_account_table',
    'update_verification_table',
    'toggle_checkbox',
    'update_status_display',
    'update_progress_display'
]
