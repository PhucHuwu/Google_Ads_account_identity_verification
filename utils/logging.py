"""
Logging utilities
"""

import time


def log_with_timestamp(message, color="black"):
    """
    Tạo log message với timestamp và icon.

    :param message: Nội dung nhật ký.
    :param color: Màu sắc hiển thị (red, yellow, green, black).
    :return: Formatted log message.
    """
    timestamp = time.strftime("%H:%M:%S", time.localtime())

    # Thêm icon tương ứng với loại thông báo
    icon = ""
    if color == "red":
        icon = "❌ "
    elif color == "yellow":
        icon = "⚠️ "
    elif color == "green":
        icon = "✅ "
    elif color == "blue":
        icon = "ℹ️ "
    elif color == "orange":
        icon = "🔄 "
    else:
        icon = ""

    return f"[{timestamp}] {icon}{message}"
