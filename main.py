import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading
import os
import pandas as pd
import pyautogui
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
    print("*Lưu ý: 1 ID sẽ là 1 luồng, nhập tối đa 10 ID và các ID phải khác nhau")
    time.sleep(10)
    exit()

df = pd.read_csv('Account_id.csv')
list_account_id = df["ID"].dropna().values.tolist()
list_account_name = df["Name"].dropna().values.tolist()


confirmation_received = threading.Event()


def account_verification(idx, account_id, name_account):
    csv1 = f'{idx + 1}.csv'
    csv2 = f'{idx + 1}_(1).csv'

    if not os.path.exists(csv1) or not os.path.exists(csv2):
        print("Hãy đảm bảo 2 file excel tồn tại")
        time.sleep(180)
        exit()
    else:
        df1 = pd.read_csv(csv1)
        df2 = pd.read_csv(csv2)

    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    ma_khach_hang_list = df1['Mã khách hàng'].tolist() + df2['Mã khách hàng'].tolist()
    name_customer_list = df1['Tài khoản'].tolist() + df2['Tài khoản'].tolist()
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
    screen_size = pyautogui.size()
    screen_width = screen_size.width
    screen_height = screen_size.height
    num_windows = len(list_account_id)

    num_cols = (1 if num_windows <= 1 else (2 if num_windows <= 3 else 4))
    num_rows = num_windows // num_cols + (1 if num_windows % num_cols != 0 else 0)
    window_width = screen_width // num_cols
    window_height = screen_height // num_rows
    driver.set_window_size(window_width, window_height)

    row = idx // num_cols
    col = idx % num_cols
    x_position = col * window_width
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

        time.sleep(10)

        try:
            click.auto_click(driver, config.arrow_drop_down_button_xpath, 30)
        except Exception:
            print(f"Lỗi 2 ở luồng {idx + 1}")
            print()
            continue

        time.sleep(2)

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

            if not df1.empty or len(df1) > 1:
                df1 = df1.drop(index=0)

            if not df2.empty or len(df2) > 1:
                df2 = df2.drop(index=0)

            df1 = pd.read_csv(csv1)
            df2 = pd.read_csv(csv2)
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

            if not df1.empty or len(df1) > 1:
                df1 = df1.drop(index=0)

            if not df2.empty or len(df2) > 1:
                df2 = df2.drop(index=0)

            df1 = pd.read_csv(csv1)
            df2 = pd.read_csv(csv2)
            continue

        print(f"Đã xác minh tài khoản {name_customer} ở luồng {idx + 1} thành công")
        print()

        if not df1.empty or len(df1) > 1:
            df1 = df1.drop(index=0)

        if not df2.empty or len(df2) > 1:
            df2 = df2.drop(index=0)

        df1 = pd.read_csv(csv1)
        df2 = pd.read_csv(csv2)

        time.sleep(15)

    print(f"Đã hoàn tất quá trình xác minh ở luồng {idx + 1}")


threads = []

for idx, (id, name) in enumerate(zip(list_account_id, list_account_name)):
    thread = threading.Thread(target=account_verification, args=(idx, id, name))
    thread.start()
    threads.append(thread)

start_program = input("Nhập 'ok' sau khi đã đăng nhập để bắt đầu quá trình xác minh tài khoản: ")
if start_program.lower() == "ok":
    confirmation_received.set()

for thread in threads:
    thread.join()
