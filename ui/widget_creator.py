"""
Widget creation functions for UI
"""

from tkinter import ttk
from screeninfo import get_monitors


def setup_window_geometry(root, expanded_width=800, expanded_height=530, collapsed_width=590, collapsed_height=280):
    """
    Thiết lập vị trí và kích thước cửa sổ.

    :param root: Tkinter root window.
    :param expanded_width: Chiều rộng khi mở rộng.
    :param expanded_height: Chiều cao khi mở rộng.
    :param collapsed_width: Chiều rộng khi thu gọn.
    :param collapsed_height: Chiều cao khi thu gọn.
    :return: Tuple (secondary_monitor, monitors).
    """
    # Tìm và thiết lập màn hình phụ nếu có
    monitors = get_monitors()
    secondary_monitor = None

    for m in monitors:
        if m.x != 0:  # Màn hình phụ có x != 0
            secondary_monitor = m
            break

    # Đặt vị trí cửa sổ ở màn hình phụ hoặc chính
    if secondary_monitor:
        x = secondary_monitor.x + (secondary_monitor.width - expanded_width) // 2
        y = secondary_monitor.y + (secondary_monitor.height - expanded_height) // 2
        root.geometry(f"{expanded_width}x{expanded_height}+{x}+{y}")
    else:
        root.geometry(f"{expanded_width}x{expanded_height}")

    # Thiết lập kích thước tối thiểu
    root.minsize(collapsed_width, collapsed_height)

    return secondary_monitor, monitors


def create_widgets(root):
    """
    Tạo các tab và thành phần giao diện chính của ứng dụng.

    :param root: Tkinter root window.
    :return: Tuple (notebook, execution_frame, account_frame, verification_frame).
    """
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)

    execution_frame = ttk.Frame(notebook)
    notebook.add(execution_frame, text="Xác minh tài khoản")

    account_frame = ttk.Frame(notebook)
    notebook.add(account_frame, text="Quản lý MCC")

    verification_frame = ttk.Frame(notebook)
    notebook.add(verification_frame, text="Quản lý tài khoản con")

    return notebook, execution_frame, account_frame, verification_frame
