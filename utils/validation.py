"""
Validation utilities
"""

import unicodedata


def check_account_name(name):
    """
    Kiểm tra tên tài khoản có hợp lệ (không dấu, không khoảng trắng).

    :param name: Tên tài khoản cần kiểm tra.
    :return: Tuple (bool, thông báo lỗi nếu có).
    """
    if ' ' in name:
        return False, "Tên tài khoản phải viết liền"

    normalized_name = unicodedata.normalize('NFKD', name)
    has_accents = any(unicodedata.combining(c) for c in normalized_name)
    if has_accents:
        return False, "Tên tài khoản không được chứa dấu"

    return True, ""
