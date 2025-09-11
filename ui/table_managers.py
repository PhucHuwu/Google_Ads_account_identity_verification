"""
Table management functions for UI
"""


def update_account_table(account_table, account_data):
    """
    Cập nhật bảng hiển thị danh sách tài khoản MCC trên giao diện.

    :param account_table: Treeview widget cho bảng tài khoản.
    :param account_data: DataFrame chứa dữ liệu tài khoản.
    """
    try:
        account_table.delete(*account_table.get_children())

        if account_data.empty:
            return

        sorted_data = account_data.copy()
        sorted_data['ID'] = sorted_data['ID'].astype(str).str.strip()
        sorted_data['Name'] = sorted_data['Name'].astype(str).str.strip()
        sorted_data = sorted_data.sort_values(by='ID')

        for _, row in sorted_data.iterrows():
            try:
                status = "☑" if row.get('Status', 0) == 1 else "☐"
                account_table.insert('', 'end', values=(status, row['ID'], row['Name']))
            except Exception:
                print(f"Lỗi khi thêm dòng {row['ID']}")

    except Exception:
        print(f"Lỗi khi cập nhật bảng")


def update_verification_table(verification_table, verification_data):
    """
    Cập nhật bảng hiển thị dữ liệu xác minh trên giao diện.

    :param verification_table: Treeview widget cho bảng xác minh.
    :param verification_data: DataFrame chứa dữ liệu xác minh.
    """
    for item in verification_table.get_children():
        verification_table.delete(item)

    if verification_data is not None:
        for i, row in verification_data.iterrows():
            if i < 100:
                verification_table.insert('', 'end', values=(row['Mã khách hàng'], row['Tài khoản']))

        if len(verification_data) > 100:
            verification_table.insert('', 'end', values=('...', f'(Còn {len(verification_data) - 100} dòng khác)'))


def toggle_checkbox(account_table, app_instance):
    """
    Xử lý sự kiện khi người dùng nhấn vào checkbox chọn tài khoản MCC.

    :param account_table: Treeview widget cho bảng tài khoản.
    :param app_instance: Instance của ứng dụng chính để truy cập account_data.
    """
    def toggle_handler(event):
        # Xác định vùng được click
        region = account_table.identify_region(event.x, event.y)
        if region == "cell":
            column = account_table.identify_column(event.x)
            if column == '#1':  # Cột checkbox
                item = account_table.identify_row(event.y)
                current_value = account_table.item(item)['values'][0]
                # Đổi trạng thái checkbox
                new_value = "☐" if current_value == "☑" else "☑"
                values = list(account_table.item(item)['values'])
                values[0] = new_value
                account_table.item(item, values=values)

                try:
                    # Cập nhật trạng thái trong DataFrame của app instance
                    account_id = str(values[1])
                    mask = app_instance.account_data['ID'].astype(str) == account_id
                    if mask.any():
                        app_instance.account_data.loc[mask, 'Status'] = 1 if new_value == "☑" else 0

                        # Lưu dữ liệu vào file
                        app_instance.save_account_data()

                        # Cập nhật UI
                        app_instance.update_status()
                        app_instance.update_spinbox_state()
                    else:
                        print(f"Không tìm thấy tài khoản với ID: {account_id}")

                except Exception as e:
                    print(f"Lỗi khi cập nhật trạng thái: {e}")
                    return

    return toggle_handler
