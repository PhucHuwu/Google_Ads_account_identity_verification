"""
Chrome driver management functions
"""

import undetected_chromedriver as uc
import os


def create_chrome_driver(idx, name_account, driver_lock, drivers):
    """
    Tạo Chrome driver với profile riêng biệt.

    :param idx: Chỉ số luồng.
    :param name_account: Tên tài khoản.
    :param driver_lock: Thread lock cho driver.
    :param drivers: Danh sách drivers.
    :return: Chrome driver instance hoặc None nếu lỗi.
    """
    try:
        options = uc.ChromeOptions()
        profile_directory = f"Profile_{idx + 1}_{name_account}"
        if not os.path.exists(profile_directory):
            os.makedirs(profile_directory)

        # Khởi tạo Chrome driver với thread-safe
        with driver_lock:
            options.user_data_dir = profile_directory
            try:
                driver = uc.Chrome(options=options)
                drivers.append(driver)
                return driver
            except Exception:
                print(f"Không thể khởi tạo Chromedriver ở luồng {idx + 1}, vui lòng update Chrome")
                return None
    except Exception as e:
        print(f"Lỗi khi tạo driver: {e}")
        return None


def setup_driver_window(driver, idx, secondary_monitor):
    """
    Thiết lập kích thước và vị trí cửa sổ browser.

    :param driver: Chrome driver instance.
    :param idx: Chỉ số luồng.
    :param secondary_monitor: Monitor phụ nếu có.
    """
    try:
        # Thiết lập vị trí và kích thước cửa sổ
        if secondary_monitor:
            window_width = secondary_monitor.width // 3
            window_height = secondary_monitor.height // 2
            position_x = secondary_monitor.x + (idx * window_width // 20) - 1600
            position_y = secondary_monitor.y
        else:
            screen_width = driver.execute_script("return window.screen.availWidth;")
            screen_height = driver.execute_script("return window.screen.availHeight;")
            window_width = screen_width // 3
            window_height = screen_height // 2
            position_x = idx * window_width // 20
            position_y = 0

        driver.set_window_size(window_width, window_height)
        driver.set_window_position(position_x, position_y)

        # Thiết lập zoom và mở Google Ads
        driver.execute_script("document.body.style.zoom='100%'")
        driver.get("https://ads.google.com/aw/overview")

    except Exception as e:
        print(f"Lỗi khi thiết lập cửa sổ: {e}")
