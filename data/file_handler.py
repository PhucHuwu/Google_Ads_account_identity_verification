"""
File handling functions
"""

import pandas as pd
from tkinter import filedialog


def browse_and_load_file():
    """
    Mở hộp thoại chọn file CSV, xử lý và lưu dữ liệu xác minh vào bcxm.csv.

    :return: Đường dẫn file được chọn hoặc None.
    """
    file_path = filedialog.askopenfilename(
        title="Chọn file CSV",
        filetypes=[("CSV files", "*.csv")]
    )

    if file_path:
        try:
            uploaded_data = pd.read_csv(file_path, skiprows=2, encoding='utf-8')
            uploaded_data.columns = uploaded_data.columns.str.strip()

            template_path = 'bcxm.csv'

            template_df = pd.DataFrame({
                'Mã khách hàng': uploaded_data['Mã khách hàng'],
                'Tài khoản': uploaded_data['Tài khoản'],
                'Trạng thái xác minh': [0] * len(uploaded_data)
            })
            template_df.to_csv(template_path, index=False)

            return template_path
        except Exception as e:
            print(f"Lỗi khi xử lý file: {e}")
            return None

    return None
