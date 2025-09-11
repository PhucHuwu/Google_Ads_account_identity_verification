"""
Verification data management functions
"""

import pandas as pd
import os


def load_verification_data():
    """
    Tải dữ liệu xác minh từ file bcxm.csv nếu tồn tại, cập nhật bảng và trạng thái.

    :return: Tuple (verification_data, verified_count, total_count).
    """
    template_path = 'bcxm.csv'

    if os.path.exists(template_path):
        try:
            df = pd.read_csv(template_path)
            verification_data = df[df['Trạng thái xác minh'] == 0]
            verified_count = len(df[df['Trạng thái xác minh'] == 1])
            total_count = len(df)
            return verification_data, verified_count, total_count
        except Exception:
            print(f"Không thể đọc file bcxm.csv")

    return None, 0, 0


def save_verification_data(verification_data):
    """
    Lưu dữ liệu xác minh vào file bcxm.csv.

    :param verification_data: DataFrame chứa dữ liệu xác minh.
    """
    template_path = 'bcxm.csv'
    try:
        verification_data.to_csv(template_path, index=False)
    except Exception as e:
        print(f"Lỗi khi lưu file xác minh: {e}")


def update_verification_status(ma_khach_hang, name_customer, status=1):
    """
    Cập nhật trạng thái xác minh cho một tài khoản.

    :param ma_khach_hang: Mã khách hàng.
    :param name_customer: Tên tài khoản khách hàng.
    :param status: Trạng thái xác minh (0 hoặc 1).
    """
    template_path = 'bcxm.csv'
    try:
        df = pd.read_csv(template_path)
        mask = (df['Mã khách hàng'] == ma_khach_hang) & (df['Tài khoản'] == name_customer)
        df.loc[mask, 'Trạng thái xác minh'] = status
        df.to_csv(template_path, index=False)
        return True
    except Exception as e:
        print(f"Không thể cập nhật trạng thái xác minh: {e}")
        return False
