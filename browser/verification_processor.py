"""
Account verification processing functions
"""

import time
import config
import click
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def process_account_verification(driver, idx, account_id, name_account, ma_khach_hang, name_customer, log_callback):
    """
    Xử lý quy trình xác minh cho một tài khoản.

    :param driver: Chrome driver instance.
    :param idx: Chỉ số luồng.
    :param account_id: ID tài khoản MCC.
    :param name_account: Tên tài khoản MCC.
    :param ma_khach_hang: Mã khách hàng.
    :param name_customer: Tên tài khoản khách hàng.
    :param log_callback: Hàm callback để ghi log.
    :return: True nếu thành công, False nếu thất bại.
    """
    try:
        # Thiết lập zoom và điều hướng
        driver.execute_script("document.body.style.zoom='50%'")
        driver.get("https://ads.google.com/aw/overview")

        log_callback(f"Luồng {idx + 1}: Đang tìm tài khoản MCC {account_id}...", "yellow")
        account_id_xpath = config.get_account_id_xpath(account_id)
        if not click.auto_click(driver, account_id_xpath, 30, log_callback=lambda msg: log_callback(f"Luồng {idx + 1}: {msg}", "black")):
            log_callback(f"Luồng {idx + 1}: Không thể tìm thấy MCC, vui lòng kiểm tra ID {account_id}", "red")
            return False

        driver.execute_script("document.body.style.zoom='50%'")
        time.sleep(5)

        # Tìm icon mũi tên chỉ xuống
        log_callback(f"Luồng {idx + 1}: Đang tìm icon mũi tên chỉ xuống...", "yellow")
        if not click.auto_click(driver, config.arrow_drop_down_button_xpath, 30, log_callback=lambda msg: log_callback(f"Luồng {idx + 1}: {msg}", "black")):
            log_callback(f"Luồng {idx + 1}: Không tìm thấy icon mũi tên chỉ xuống", "red")
            return False

        time.sleep(3)

        # Tìm icon kính lúp
        log_callback(f"Luồng {idx + 1}: Đang tìm icon kính lúp...", "yellow")
        if not click.auto_click(driver, config.search_button_xpath, 30, log_callback=lambda msg: log_callback(f"Luồng {idx + 1}: {msg}", "black")):
            log_callback(f"Luồng {idx + 1}: Không thể tìm thấy icon kính lúp", "red")
            return False

        # Nhập mã khách hàng
        ActionChains(driver).send_keys(f"{ma_khach_hang}").perform()
        time.sleep(3)

        # Click vào tên khách hàng
        log_callback(f"Luồng {idx + 1}: Đang tìm tài khoản khách hàng {name_customer}...", "yellow")
        customer_xpath = config.get_customer_name_xpath(name_customer)
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, customer_xpath))
        )
        driver.execute_script("arguments[0].click();", element)
        log_callback(f"Luồng {idx + 1}: Đã tìm thấy và click vào tài khoản {name_customer}", "green")

        time.sleep(5)

        # Truy cập mục thanh toán
        log_callback(f"Luồng {idx + 1}: Đang tìm mục thanh toán...", "yellow")
        if not click.auto_click(driver, config.pay_button_xpath, 30, log_callback=lambda msg: log_callback(f"Luồng {idx + 1}: {msg}", "black")):
            log_callback(f"Luồng {idx + 1}: Không thể truy cập vào mục thanh toán", "red")
            return False

        # Click vào quy trình xác minh
        log_callback(f"Luồng {idx + 1}: Đang tìm mục quy trình xác minh...", "yellow")
        if not click.auto_click(driver, config.verification_process_button_xpath, 10, log_callback=lambda msg: log_callback(f"Luồng {idx + 1}: {msg}", "black")):
            log_callback(f"Luồng {idx + 1}: Không thể click vào mục quy trình xác minh", "red")
            return False

        time.sleep(5)
        return True

    except Exception as e:
        log_callback(f"Luồng {idx + 1}: Lỗi khi xử lý tài khoản {name_customer}: {str(e)}", "red")
        return False
