"""
Application initialization functions
"""

import tkinter as tk
from tkinter import ttk
import threading
import pandas as pd
from utils import kill_existing_chrome_drivers
from ui.widget_creator import setup_window_geometry, create_widgets


def initialize_app_variables():
    """
    Khởi tạo các biến thread-safe và dữ liệu.

    :return: Dictionary chứa các biến đã khởi tạo.
    """
    variables = {
        'drivers': [],
        'threads': [],
        'driver_lock': threading.Lock(),
        'file_lock': threading.Lock(),
        'confirmation_received': threading.Event(),
        'is_running': False,
        'account_data': pd.DataFrame(columns=['ID', 'Name', 'Status']),
        'verification_data': None,
        'thread_count': tk.IntVar(value=1),
        'login_checked': tk.BooleanVar(value=True),
        'verified_count': 0,
        'verified_count_lock': threading.Lock(),
        'is_collapsed': False
    }
    return variables


def setup_app_style():
    """
    Thiết lập style cho giao diện.

    :return: Style object.
    """
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 10))
    style.configure('TLabel', font=('Arial', 10))
    style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
    return style


def initialize_app(root):
    """
    Khởi tạo ứng dụng với các thiết lập cơ bản.

    :param root: Tkinter root window.
    :return: Tuple (variables, style, secondary_monitor, monitors, widgets).
    """
    # Đóng tất cả Chrome driver đang chạy trước khi khởi tạo
    kill_existing_chrome_drivers()

    root.title("Google Ads Verification Tool")

    # Thiết lập vị trí và kích thước cửa sổ
    secondary_monitor, monitors = setup_window_geometry(root)

    # Khởi tạo các biến
    variables = initialize_app_variables()

    # Thiết lập style
    style = setup_app_style()

    # Tạo các widget
    widgets = create_widgets(root)

    return variables, style, secondary_monitor, monitors, widgets
