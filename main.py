import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading
import os
import pandas as pd
import click
import config

driver_lock = threading.Lock()

if not os.path.exists('Account_id.csv'):
    data = {
        'ID': [],
        'Name': []
    }
    df = pd.DataFrame(data)
    df.to_csv('Account_id.csv', index=False)
    print("File excel vừa được tạo, vui lòng thêm ID vào file excel")
    print("*Lưu ý: 1 ID sẽ là 1 luồng, nhập tối đa 10 ID")
    time.sleep(10)
    exit()

df = pd.read_csv('Account_id.csv')
list_account_id = df["ID"].dropna().values.tolist()
list_account_name = df["Name"].dropna().values.tolist()


confirmation_received = threading.Event()


def account_verification(idx, account_id, name_account):
    csv = f'excel/{idx + 1}.csv'

    if not os.path.exists(csv):
        print(f"Hãy đảm bảo file excel của luồng {idx + 1} tồn tại")
        time.sleep(180)
        exit()
    else:
        df = pd.read_csv(csv)

    df.columns = df.columns.str.strip()

    ma_khach_hang_list = df['Mã khách hàng'].tolist()
    name_customer_list = df['Tài khoản'].tolist()
    # ------------------------------------------------------------------------------------------------------------------
    options = uc.ChromeOptions()
    profile_directory = f"Profile_{idx + 1}_{name_account}"
    if not os.path.exists(profile_directory):
        os.makedirs(profile_directory)

    with driver_lock:
        options.user_data_dir = profile_directory
        try:
            driver = uc.Chrome(options=options)
        except Exception:
            print(f"Lỗi 1 ở luồng {idx + 1}")
            time.sleep(180)
            exit()
    # ------------------------------------------------------------------------------------------------------------------
    screen_width = driver.execute_script("return window.screen.availWidth;")
    screen_height = driver.execute_script("return window.screen.availHeight;")

    num_cols = 10
    num_rows = 1
    window_width = screen_width // num_cols
    window_height = screen_height // num_rows // 2
    driver.set_window_size(window_width, window_height)

    row = idx // num_cols
    col = idx % num_cols
    x_position = col * window_width // 2
    y_position = row * window_height
    driver.set_window_position(x_position, y_position)
    # ------------------------------------------------------------------------------------------------------------------
    driver.get("https://ads.google.com/aw/overview")
    confirmation_received.wait()
    # ------------------------------------------------------------------------------------------------------------------
    for ma_khach_hang, name_customer in zip(ma_khach_hang_list, name_customer_list):
        driver.get("https://ads.google.com/aw/overview")

        try:
            click.auto_click(driver, "//span[text()='" + account_id + "']", 30)
        except Exception:
            print(f"Lỗi 1 ở luồng {idx + 1}")
            print()
            continue

        time.sleep(5)

        try:
            click.auto_click(driver, config.arrow_drop_down_button_xpath, 30)
        except Exception:
            print(f"Lỗi 2 ở luồng {idx + 1}")
            print()
            continue

        time.sleep(3)

        try:
            click.auto_click(driver, config.search_button_xpath, 30)
        except Exception:
            print(f"Lỗi 3 ở luồng {idx + 1}")
            print()
            continue

        ActionChains(driver).send_keys(f"{ma_khach_hang}").perform()
        time.sleep(3)

        try:
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//a[contains(@class, 'customer-title') and div//div[contains(@class, 'customer-name') and text()='" + name_customer + "']]"))
            )
            driver.execute_script("arguments[0].click();", element)
        except Exception:
            print(f"Lỗi 4 ở luồng {idx + 1}")
            print()
            continue

        time.sleep(5)

        try:
            click.auto_click(driver, config.pay_button_xpath, 30)
        except Exception:
            print(f"Lỗi 5 ở luồng {idx + 1}")
            print()
            continue

        try:
            click.auto_click(driver, config.verification_process_button_xpath, 10)
        except Exception:
            print(f"Lỗi 6 ở luồng {idx + 1}")
            print()
            continue

        time.sleep(5)

        try:
            click.auto_click(driver, config.start_verification_button_xpath, 5)
        except Exception:
            print(f"Lỗi 7 ở luồng {idx + 1}")
            print()

            if not df.empty or len(df) > 1:
                df = df.drop(index=0)

            df = pd.read_csv(csv)
            continue

        try:
            click.auto_click(driver, config.check_box_1_xpath, 5)
        except Exception:
            pass

        time.sleep(1)

        try:
            click.auto_click(driver, config.check_box_2_xpath, 5)
        except Exception:
            pass

        try:
            click.auto_click(driver, config.save_and_continue_button_xpath, 10)
        except Exception:
            print(f"Lỗi 8 ở luồng {idx + 1}")
            print()

            if not df.empty or len(df) > 1:
                df = df.drop(index=0)

            df = pd.read_csv(csv)
            continue

        print(f"Đã xác minh tài khoản {name_customer} ở luồng {idx + 1} thành công")
        print()

        if not df.empty or len(df) > 1:
            df = df.drop(index=0)

        df = pd.read_csv(csv)

        time.sleep(15)

    print(f"Đã hoàn tất quá trình xác minh ở luồng {idx + 1}")


threads = []

for idx, (id, name) in enumerate(zip(list_account_id, list_account_name)):
    thread = threading.Thread(target=account_verification, args=(idx, id, name))
    thread.start()
    time.sleep(1)
    threads.append(thread)

start_program = input("Nhập 'ok' sau khi đã đăng nhập để bắt đầu quá trình xác minh tài khoản: ")
if start_program.lower() == "ok":
    confirmation_received.set()

for thread in threads:
    thread.join()
