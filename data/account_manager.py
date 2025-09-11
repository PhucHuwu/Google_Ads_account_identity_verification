"""
Account data management functions
"""

import pandas as pd
import os


def load_account_data():
    """
    Tải dữ liệu tài khoản MCC từ file Account_id.csv nếu tồn tại.

    :return: DataFrame chứa dữ liệu tài khoản.
    """
    if os.path.exists('Account_id.csv'):
        try:
            return pd.read_csv('Account_id.csv')
        except Exception:
            print(f"Không thể đọc file Account_id.csv")

    return pd.DataFrame(columns=['ID', 'Name', 'Status'])


def save_account_data(account_data, retry_count=3):
    """
    Lưu dữ liệu tài khoản MCC vào file Account_id.csv, thử lại nếu gặp lỗi.

    :param account_data: DataFrame chứa dữ liệu tài khoản.
    :param retry_count: Số lần thử lưu file.
    :return: True nếu lưu thành công, False nếu thất bại.
    """
    for attempt in range(retry_count):
        try:
            account_data.to_csv('Account_id.csv', index=False)
            return True
        except Exception:
            if attempt < retry_count - 1:
                print(f"Lần {attempt + 1}: Không thể lưu file, đang thử lại...")
            else:
                print(f"Không thể lưu danh sách tài khoản vào file Account_id.csv")
                return False
