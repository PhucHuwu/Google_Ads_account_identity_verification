"""
Chrome driver management utilities
"""

import psutil


def kill_existing_chrome_drivers():
    """
    Đóng tất cả các tiến trình Chrome driver đang chạy để tránh xung đột khi khởi động ứng dụng.
    """
    try:
        # Lặp qua tất cả các tiến trình đang chạy
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] and 'chrome.exe' in proc.info['name'].lower():
                try:
                    cmdline = proc.cmdline()
                    # Kiểm tra nếu có port debug remote
                    if any('--remote-debugging-port=' in arg for arg in cmdline):
                        proc.terminate()  # Đóng tiến trình Chrome driver
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
    except Exception:
        print(f"Lỗi khi đóng Chrome")
