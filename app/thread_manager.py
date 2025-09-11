"""
Thread management functions for the application
"""

import threading
import time
import numpy as np
from browser import create_chrome_driver, setup_driver_window, process_account_verification, check_and_execute_tasks
from data import update_verification_status


def account_verification_thread(app_instance, idx, account_id, name_account, chunk):
    """
    Luồng thực hiện xác minh danh tính cho một phần dữ liệu tài khoản con.

    :param app_instance: Instance của ứng dụng chính.
    :param idx: Chỉ số luồng.
    :param account_id: ID tài khoản MCC.
    :param name_account: Tên tài khoản MCC.
    :param chunk: Phần dữ liệu xác minh được giao cho luồng này.
    """
    driver = None
    try:
        # Tạo Chrome driver
        driver = create_chrome_driver(idx, name_account, app_instance.driver_lock, app_instance.drivers)
        if not driver:
            return

        # Thiết lập cửa sổ browser
        setup_driver_window(driver, idx, app_instance.secondary_monitor)

        # Chờ xác nhận đăng nhập
        if not app_instance.login_checked.get():
            app_instance.log_from_thread(f"Luồng {idx + 1}: Vui lòng đăng nhập", "yellow")

        app_instance.confirmation_received.wait()

        if not app_instance.is_running:
            return

        # Xử lý từng tài khoản trong chunk
        for index, row in chunk.iterrows():
            if not app_instance.is_running:
                return

            ma_khach_hang = row['Mã khách hàng']
            name_customer = row['Tài khoản']

            # Ghi nhận thời điểm bắt đầu xử lý tài khoản
            account_start_time = time.time()

            try:
                # Xử lý quy trình xác minh
                if not process_account_verification(driver, idx, account_id, name_account, ma_khach_hang, name_customer,
                                                    lambda msg, color="black": app_instance._get_color_callback(idx, msg)):
                    continue

                # Xử lý các nhiệm vụ
                if not check_and_execute_tasks(driver, idx, name_customer,
                                               lambda msg, color="black": app_instance._get_color_callback(idx, msg)):
                    continue

                # Cập nhật trạng thái xác minh thành công
                if update_verification_status(ma_khach_hang, name_customer, 1):
                    app_instance.increment_verified_count()

                # Tính toán thời gian thực hiện
                account_end_time = time.time()
                execution_time = account_end_time - account_start_time
                minutes = int(execution_time // 60)
                seconds = int(execution_time % 60)

                if minutes > 0:
                    time_str = f"{minutes} phút {seconds} giây"
                else:
                    time_str = f"{seconds} giây"

                app_instance.log_from_thread(f"Luồng {idx + 1}: Đã xác minh tài khoản {name_customer} thành công (Thời gian: {time_str})", "green")

                # Delay giữa các tài khoản
                if app_instance.thread_count.get() == 1:
                    time.sleep(10)
                else:
                    time.sleep(30)

            except Exception:
                app_instance.log_from_thread(f"Luồng {idx + 1}: Lỗi khi xác minh tài khoản {name_customer}", "red")
                continue

        app_instance.log_from_thread(f"Luồng {idx + 1}: Đã hoàn tất xác minh tất cả các tài khoản được giao", "green")

        # Kiểm tra và reset UI nếu tất cả luồng hoàn thành
        with app_instance.driver_lock:
            app_instance.drivers.remove(driver)
            if not app_instance.drivers:
                app_instance.root.after(0, lambda: app_instance.reset_ui_after_completion())

    except Exception as e:
        app_instance.log_from_thread(f"Luồng {idx + 1}: Lỗi không xác định: {str(e)}", "red")

    finally:
        # Đóng driver và cleanup
        try:
            if driver:
                driver.quit()
                with app_instance.driver_lock:
                    if driver in app_instance.drivers:
                        app_instance.drivers.remove(driver)
        except Exception:
            pass


def start_verification_threads(app_instance):
    """
    Khởi động các luồng xác minh tài khoản con.

    :param app_instance: Instance của ứng dụng chính.
    """
    # Lấy danh sách tài khoản MCC được chọn
    selected_accounts = app_instance.account_data[app_instance.account_data['Status'] == 1]
    if len(selected_accounts) == 0:
        return False

    # Đọc file dữ liệu xác minh
    try:
        import pandas as pd
        template_path = 'bcxm.csv'
        verification_df = pd.read_csv(template_path)
        unverified_accounts = verification_df[verification_df['Trạng thái xác minh'] == 0]

        if len(unverified_accounts) == 0:
            return False

        app_instance.verification_data = unverified_accounts
    except Exception:
        return False

    try:
        # Chia dữ liệu theo số luồng
        chunks = np.array_split(app_instance.verification_data, app_instance.thread_count.get())

        # Thiết lập trạng thái đang chạy
        app_instance.is_running = True
        app_instance.status_label.config(text="Đang thực hiện...")
        app_instance.start_btn.config(state='disabled')

        # Xử lý trạng thái đăng nhập
        if not app_instance.login_checked.get():
            app_instance.confirm_btn.config(state='normal')
        else:
            app_instance.confirmation_received.set()
            app_instance.confirm_btn.config(state='disabled')

        # Chuẩn bị danh sách tài khoản cho các luồng
        app_instance.threads = []
        list_account_id = []
        list_account_name = []

        if len(selected_accounts) == 1:
            # Một tài khoản cho nhiều luồng
            account = selected_accounts.iloc[0]
            list_account_id = [account['ID']] * app_instance.thread_count.get()
            list_account_name = [account['Name']] * app_instance.thread_count.get()
        else:
            # Mỗi luồng một tài khoản
            list_account_id = selected_accounts['ID'].tolist()
            list_account_name = selected_accounts['Name'].tolist()

        # Khởi tạo và chạy các luồng
        for idx, ((account_id, name_account), chunk) in enumerate(zip(
                zip(list_account_id, list_account_name),
                chunks)):
            thread = threading.Thread(
                target=account_verification_thread,
                args=(app_instance, idx, account_id, name_account, chunk)
            )
            thread.daemon = True
            thread.start()
            app_instance.threads.append(thread)
            time.sleep(1)  # Delay giữa các luồng

        return True

    except Exception:
        app_instance.log(f"Lỗi khi khởi động trình duyệt")
        return False
