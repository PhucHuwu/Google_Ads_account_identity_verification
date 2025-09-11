"""
Tab setup functions for UI
"""

import tkinter as tk
from tkinter import ttk
from .table_managers import toggle_checkbox


def setup_account_tab(parent, app_instance):
    """
    Thiết lập tab quản lý tài khoản MCC, bao gồm nhập thông tin và bảng hiển thị.

    :param parent: Frame cha chứa tab này.
    :param app_instance: Instance của ứng dụng chính.
    """
    header_label = ttk.Label(parent, text="Quản lý tài khoản MCC", style='Header.TLabel')
    header_label.pack(pady=10)

    input_frame = ttk.Frame(parent)
    input_frame.pack(fill='x', padx=20, pady=10)

    ttk.Label(input_frame, text="ID tài khoản:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    app_instance.id_entry = ttk.Entry(input_frame, width=35)
    app_instance.id_entry.insert(0, "123-456-7890")
    app_instance.id_entry.config(foreground='gray')
    app_instance.id_entry.bind('<FocusIn>', lambda e: app_instance._on_id_entry_focus_in())
    app_instance.id_entry.bind('<FocusOut>', lambda e: app_instance._on_id_entry_focus_out())
    app_instance.id_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Tên tài khoản:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    app_instance.name_entry = ttk.Entry(input_frame, width=35)
    app_instance.name_entry.insert(0, "Tên tài khoản viết liền không dấu")
    app_instance.name_entry.config(foreground='gray')
    app_instance.name_entry.bind('<FocusIn>', lambda e: app_instance._on_name_entry_focus_in())
    app_instance.name_entry.bind('<FocusOut>', lambda e: app_instance._on_name_entry_focus_out())
    app_instance.name_entry.grid(row=1, column=1, padx=5, pady=5)

    add_btn = ttk.Button(input_frame, text="Thêm tài khoản", command=app_instance.add_account)
    add_btn.grid(row=0, column=2, columnspan=2, pady=10, sticky='w')

    remove_btn = ttk.Button(input_frame, text="Xóa tài khoản đã chọn", command=app_instance.remove_account)
    remove_btn.grid(row=1, column=2, columnspan=2, pady=10, sticky='w')

    table_frame = ttk.Frame(parent)
    table_frame.pack(fill='both', expand=True, padx=20, pady=10)

    columns = ('selected', 'id', 'name')
    app_instance.account_table = ttk.Treeview(table_frame, columns=columns, show='headings')
    app_instance.account_table.heading('selected', text='')
    app_instance.account_table.heading('id', text='ID tài khoản')
    app_instance.account_table.heading('name', text='Tên tài khoản')
    app_instance.account_table.column('selected', width=50)
    app_instance.account_table.column('id', width=150)
    app_instance.account_table.column('name', width=250)
    app_instance.account_table.pack(side='left', fill='both', expand=True)

    # Bind toggle checkbox event
    toggle_handler = toggle_checkbox(app_instance.account_table, app_instance)
    app_instance.account_table.bind('<Button-1>', toggle_handler)

    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=app_instance.account_table.yview)
    scrollbar.pack(side='right', fill='y')
    app_instance.account_table.configure(yscrollcommand=scrollbar.set)


def setup_verification_tab(parent, app_instance):
    """
    Thiết lập tab quản lý file báo cáo xác minh danh tính.

    :param parent: Frame cha chứa tab này.
    :param app_instance: Instance của ứng dụng chính.
    """
    header_label = ttk.Label(parent, text="Cấu hình file báo cáo xác minh danh tính", style='Header.TLabel')
    header_label.pack(pady=10)

    info_label = ttk.Label(parent, text="Chọn hoặc tạo file CSV chứa danh sách tài khoản con cần xác minh")
    info_label.pack(pady=5)

    file_frame = ttk.Frame(parent)
    file_frame.pack(fill='x', padx=20, pady=10)

    app_instance.file_path_var = tk.StringVar()
    file_path_entry = ttk.Entry(file_frame, textvariable=app_instance.file_path_var, width=50)
    file_path_entry.pack(side='left', padx=5, fill='x', expand=True)

    browse_btn = ttk.Button(file_frame, text="Chọn file", command=app_instance.browse_file)
    browse_btn.pack(side='left', padx=5)

    preview_label = ttk.Label(parent, text="Xem trước dữ liệu:")
    preview_label.pack(anchor='w', padx=20, pady=5)

    table_frame = ttk.Frame(parent)
    table_frame.pack(fill='both', expand=True, padx=20, pady=10)

    columns = ('ma_khach_hang', 'tai_khoan')
    app_instance.verification_table = ttk.Treeview(table_frame, columns=columns, show='headings')
    app_instance.verification_table.heading('ma_khach_hang', text='Mã khách hàng')
    app_instance.verification_table.heading('tai_khoan', text='Tài khoản')
    app_instance.verification_table.column('ma_khach_hang', width=150)
    app_instance.verification_table.column('tai_khoan', width=250)
    app_instance.verification_table.pack(side='left', fill='both', expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=app_instance.verification_table.yview)
    scrollbar.pack(side='right', fill='y')
    app_instance.verification_table.configure(yscrollcommand=scrollbar.set)


def setup_execution_tab(parent, app_instance):
    """
    Thiết lập tab thực thi quy trình xác minh, bao gồm trạng thái, điều khiển và nhật ký.

    :param parent: Frame cha chứa tab này.
    :param app_instance: Instance của ứng dụng chính.
    """
    header_label = ttk.Label(parent, text="Thực thi quy trình xác minh", style='Header.TLabel')
    header_label.pack(pady=10)

    status_frame = ttk.LabelFrame(parent, text="Trạng thái")
    status_frame.pack(fill='x', padx=20, pady=10)

    ttk.Label(status_frame, text="Số tài khoản MCC đã chọn:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    app_instance.mcc_count_label = ttk.Label(status_frame, text="0")
    app_instance.mcc_count_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    ttk.Label(status_frame, text="Số tài khoản cần xác minh:").grid(
        row=0, column=3, padx=5, pady=5, sticky='w')
    app_instance.verification_count_label = ttk.Label(status_frame, text="0/0")
    app_instance.verification_count_label.grid(row=0, column=4, padx=5, pady=5, sticky='e')

    ttk.Label(status_frame, text="Số luồng:").grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')
    app_instance.thread_spinbox = ttk.Spinbox(
        status_frame,
        from_=1,
        to=100,
        width=5,
        textvariable=app_instance.thread_count,
        state='readonly'
    )
    app_instance.thread_spinbox.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='w')

    ttk.Label(status_frame, text="Số tài khoản đã xác minh:").grid(
        row=1, column=3, padx=5, pady=5, sticky='w')
    app_instance.verified_count_label = ttk.Label(status_frame, text="0/0")
    app_instance.verified_count_label.grid(row=1, column=4, padx=5, pady=5, sticky='e')

    app_instance.login_check = ttk.Checkbutton(
        status_frame,
        text="Đã đăng nhập",
        variable=app_instance.login_checked
    )
    app_instance.login_check.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='w')

    ttk.Label(status_frame, text="Trạng thái:").grid(row=4, column=3, padx=5, pady=5, sticky='w')
    app_instance.status_label = ttk.Label(status_frame, text="Chưa bắt đầu")
    app_instance.status_label.grid(row=4, column=4, padx=5, pady=5, sticky='w')

    control_frame = ttk.Frame(parent)
    control_frame.pack(fill='x', padx=20, pady=10)

    app_instance.start_btn = ttk.Button(control_frame, text="Bắt đầu xác minh", command=app_instance.start_browsers)
    app_instance.start_btn.pack(side='left', padx=5)

    app_instance.confirm_btn = ttk.Button(control_frame, text="Xác nhận đã đăng nhập", command=app_instance.confirm_login, state='disabled')
    app_instance.confirm_btn.pack(side='left', padx=5)

    log_frame = ttk.LabelFrame(parent, text="Nhật ký hoạt động")
    log_frame.pack(fill='both', expand=True, padx=20, pady=10)

    app_instance.log_text = tk.Text(log_frame, height=10, wrap='word', state='disabled')
    app_instance.log_text.pack(side='left', fill='both', expand=True)

    log_scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=app_instance.log_text.yview)
    log_scrollbar.pack(side='right', fill='y')
    app_instance.log_text.configure(yscrollcommand=log_scrollbar.set)

    progress_frame = ttk.Frame(parent)
    progress_frame.pack(fill='x', padx=20, pady=10)

    ttk.Label(progress_frame, text="Tiến độ xác minh:").pack(side='left')
    app_instance.progress_var = tk.DoubleVar()
    app_instance.progress_bar = ttk.Progressbar(progress_frame, variable=app_instance.progress_var, maximum=100)
    app_instance.progress_bar.pack(side='left', fill='x', expand=True, padx=5)
    app_instance.progress_percent = ttk.Label(progress_frame, text="0%")
    app_instance.progress_percent.pack(side='left')
