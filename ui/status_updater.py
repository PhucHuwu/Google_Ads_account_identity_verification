"""
Status update functions for UI
"""

import os
import pandas as pd


def update_status_display(mcc_count_label, verification_count_label, verified_count_label, account_data):
    """
    Cập nhật các nhãn trạng thái về số lượng tài khoản MCC, xác minh, đã xác minh.

    :param mcc_count_label: Label hiển thị số tài khoản MCC.
    :param verification_count_label: Label hiển thị số tài khoản cần xác minh.
    :param verified_count_label: Label hiển thị số tài khoản đã xác minh.
    :param account_data: DataFrame chứa dữ liệu tài khoản.
    """
    selected_mcc_count = len(account_data[account_data['Status'] == 1])
    mcc_count_label.config(text=str(selected_mcc_count))

    try:
        template_path = 'bcxm.csv'
        if os.path.exists(template_path):
            df = pd.read_csv(template_path)
            total_accounts = len(df)
            verified_accounts = len(df[df['Trạng thái xác minh'] == 1])
            unverified_accounts = len(df[df['Trạng thái xác minh'] == 0])

            verification_count_label.config(text=f"{unverified_accounts}/{total_accounts}")
            verified_count_label.config(text=f"{verified_accounts}/{total_accounts}")
    except Exception:
        print(f"Lỗi khi cập nhật trạng thái")
        verification_count_label.config(text="0/0")
        verified_count_label.config(text="0/0")


def update_progress_display(progress_var, progress_percent, status_label, start_btn, confirm_btn, verified_count, total_count):
    """
    Cập nhật hiển thị tiến độ xác minh.

    :param progress_var: Biến tiến độ.
    :param progress_percent: Label hiển thị phần trăm.
    :param status_label: Label trạng thái.
    :param start_btn: Nút bắt đầu.
    :param confirm_btn: Nút xác nhận.
    :param verified_count: Số tài khoản đã xác minh.
    :param total_count: Tổng số tài khoản.
    """
    if total_count > 0:
        progress = (verified_count / total_count) * 100
        progress_var.set(progress)
        progress_percent.config(text=f"{int(progress)}%")

        if progress >= 100:
            status_label.config(text="Hoàn thành")
            start_btn.config(state='normal')
            confirm_btn.config(state='disabled')
    else:
        progress_var.set(0)
        progress_percent.config(text="0%")
