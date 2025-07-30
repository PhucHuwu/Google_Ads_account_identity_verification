import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import threading
import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import config
import click
import psutil
from screeninfo import get_monitors


class GoogleAdsVerificationApp:
    EXPANDED_WIDTH = 800
    EXPANDED_HEIGHT = 530

    COLLAPSED_WIDTH = 590
    COLLAPSED_HEIGHT = 280

    def kill_existing_chrome_drivers():
        """
        Đóng tất cả các tiến trình Chrome driver đang chạy để tránh xung đột khi khởi động ứng dụng.
        """
        try:
            # Lặp qua tất cả các tiến trình đang chạy
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and 'chrome.exe' in proc.info['name'].lower():
                    try:
                        cmdline = proc.cmdline()
                        # Kiểm tra nếu có port debug remote
                        if any('--remote-debugging-port=' in arg for arg in cmdline):
                            proc.terminate()  # Đóng tiến trình Chrome driver
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
        except Exception:
            print(f"Lỗi khi đóng Chrome")

    def __init__(self, root):
        """
        Khởi tạo ứng dụng, thiết lập giao diện, trạng thái ban đầu và tải dữ liệu nếu có.

        :param root: Đối tượng Tkinter root window.
        """
        # Đóng tất cả Chrome driver đang chạy trước khi khởi tạo
        GoogleAdsVerificationApp.kill_existing_chrome_drivers()

        self.root = root
        self.root.title("Google Ads Verification Tool")

        # Tìm và thiết lập màn hình phụ nếu có
        self.monitors = get_monitors()
        self.secondary_monitor = None

        for m in self.monitors:
            if m.x != 0:  # Màn hình phụ có x != 0
                self.secondary_monitor = m
                break

        # Đặt vị trí cửa sổ ở màn hình phụ hoặc chính
        if self.secondary_monitor:
            x = self.secondary_monitor.x + (self.secondary_monitor.width - self.EXPANDED_WIDTH) // 2
            y = self.secondary_monitor.y + (self.secondary_monitor.height - self.EXPANDED_HEIGHT) // 2
            self.root.geometry(f"{self.EXPANDED_WIDTH}x{self.EXPANDED_HEIGHT}+{x}+{y}")
        else:
            self.root.geometry(f"{self.EXPANDED_WIDTH}x{self.EXPANDED_HEIGHT}")

        # Thiết lập kích thước tối thiểu
        self.root.minsize(self.COLLAPSED_WIDTH, self.COLLAPSED_HEIGHT)

        self.is_collapsed = False

        # Khởi tạo các biến thread-safe
        self.drivers = []
        self.threads = []
        self.driver_lock = threading.Lock()
        self.file_lock = threading.Lock()
        self.confirmation_received = threading.Event()
        self.is_running = False

        # Khởi tạo DataFrame cho dữ liệu tài khoản
        self.account_data = pd.DataFrame(columns=['ID', 'Name', 'Status'])
        self.verification_data = None
        self.thread_count = tk.IntVar(value=1)
        self.thread_spinbox = None
        self.login_checked = tk.BooleanVar(value=True)
        self.verified_count = 0
        self.verified_count_lock = threading.Lock()

        # Thiết lập style cho giao diện
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))

        # Tạo các widget giao diện
        self.create_widgets()

        # Tạo nút thu gọn cửa sổ
        self.collapse_button = ttk.Button(self.root, text="Thu gọn", command=self.collapse_window)
        self.collapse_button.place(relx=1.0, y=0, anchor='ne')

        # Tải dữ liệu có sẵn từ file
        self.load_existing_data()
        self.load_existing_verification_data()

        # Hiển thị thông báo chào mừng
        self.log("Chào mừng bạn đến với tool xác minh danh tính Google Ads! (´▽`ʃ♡ƪ)")
        self.log("Made by: Phuc TranHuwu ( •̀ ω •́ )✧")
        self.log("Vui lòng thêm MCC và tải lên file báo cáo xác minh danh tính để bắt đầu.")

    def create_widgets(self):
        """
        Tạo các tab và thành phần giao diện chính của ứng dụng.
        """
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        execution_frame = ttk.Frame(notebook)
        notebook.add(execution_frame, text="Xác minh tài khoản")

        account_frame = ttk.Frame(notebook)
        notebook.add(account_frame, text="Quản lý MCC")

        verification_frame = ttk.Frame(notebook)
        notebook.add(verification_frame, text="Quản lý tài khoản con")

        self.setup_account_tab(account_frame)

        self.setup_verification_tab(verification_frame)

        self.setup_execution_tab(execution_frame)

    def setup_account_tab(self, parent):
        """
        Thiết lập tab quản lý tài khoản MCC, bao gồm nhập thông tin và bảng hiển thị.

        :param parent: Frame cha chứa tab này.
        """
        header_label = ttk.Label(parent, text="Quản lý tài khoản MCC", style='Header.TLabel')
        header_label.pack(pady=10)

        input_frame = ttk.Frame(parent)
        input_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(input_frame, text="ID tài khoản:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.id_entry = ttk.Entry(input_frame, width=35)
        self.id_entry.insert(0, "123-456-7890")
        self.id_entry.config(foreground='gray')
        self.id_entry.bind('<FocusIn>', lambda e: self._on_id_entry_focus_in())
        self.id_entry.bind('<FocusOut>', lambda e: self._on_id_entry_focus_out())
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Tên tài khoản:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.name_entry = ttk.Entry(input_frame, width=35)
        self.name_entry.insert(0, "Tên tài khoản viết liền không dấu")
        self.name_entry.config(foreground='gray')
        self.name_entry.bind('<FocusIn>', lambda e: self._on_name_entry_focus_in())
        self.name_entry.bind('<FocusOut>', lambda e: self._on_name_entry_focus_out())
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        add_btn = ttk.Button(input_frame, text="Thêm tài khoản", command=self.add_account)
        add_btn.grid(row=0, column=2, columnspan=2, pady=10, sticky='w')

        remove_btn = ttk.Button(input_frame, text="Xóa tài khoản đã chọn", command=self.remove_account)
        remove_btn.grid(row=1, column=2, columnspan=2, pady=10, sticky='w')

        table_frame = ttk.Frame(parent)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)

        columns = ('selected', 'id', 'name')
        self.account_table = ttk.Treeview(table_frame, columns=columns, show='headings')
        self.account_table.heading('selected', text='')
        self.account_table.heading('id', text='ID tài khoản')
        self.account_table.heading('name', text='Tên tài khoản')
        self.account_table.column('selected', width=50)
        self.account_table.column('id', width=150)
        self.account_table.column('name', width=250)
        self.account_table.pack(side='left', fill='both', expand=True)

        self.account_table.bind('<Button-1>', self.toggle_checkbox)

        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.account_table.yview)
        scrollbar.pack(side='right', fill='y')
        self.account_table.configure(yscrollcommand=scrollbar.set)

    def toggle_checkbox(self, event):
        """
        Xử lý sự kiện khi người dùng nhấn vào checkbox chọn tài khoản MCC.

        :param event: Sự kiện click chuột.
        """
        # Xác định vùng được click
        region = self.account_table.identify_region(event.x, event.y)
        if region == "cell":
            column = self.account_table.identify_column(event.x)
            if column == '#1':  # Cột checkbox
                item = self.account_table.identify_row(event.y)
                current_value = self.account_table.item(item)['values'][0]
                # Đổi trạng thái checkbox
                new_value = "☐" if current_value == "☑" else "☑"
                values = list(self.account_table.item(item)['values'])
                values[0] = new_value
                self.account_table.item(item, values=values)

                try:
                    # Cập nhật trạng thái trong DataFrame
                    idx = self.account_data.index[self.account_data['ID'].astype(str) == str(values[1])].tolist()[0]
                    self.account_data.at[idx, 'Status'] = 1 if new_value == "☑" else 0

                    # Lưu dữ liệu vào file
                    self.save_account_data()
                except Exception:
                    self.log(f"Lỗi khi cập nhật trạng thái")
                    return

                # Đếm số tài khoản được chọn
                selected_count = sum(1 for item in self.account_table.get_children()
                                     if self.account_table.item(item)['values'][0] == "☑")

                # Điều chỉnh spinbox số luồng theo số tài khoản được chọn
                if selected_count > 1:
                    self.thread_spinbox.configure(state='disabled')
                    self.thread_count.set(selected_count)
                else:
                    self.thread_spinbox.configure(state='readonly')
                    if selected_count == 0:
                        self.thread_count.set(1)

    def setup_verification_tab(self, parent):
        """
        Thiết lập tab quản lý file báo cáo xác minh danh tính.

        :param parent: Frame cha chứa tab này.
        """
        header_label = ttk.Label(parent, text="Cấu hình file báo cáo xác minh danh tính", style='Header.TLabel')
        header_label.pack(pady=10)

        info_label = ttk.Label(parent, text="Chọn hoặc tạo file CSV chứa danh sách tài khoản con cần xác minh")
        info_label.pack(pady=5)

        file_frame = ttk.Frame(parent)
        file_frame.pack(fill='x', padx=20, pady=10)

        self.file_path_var = tk.StringVar()
        file_path_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=50)
        file_path_entry.pack(side='left', padx=5, fill='x', expand=True)

        browse_btn = ttk.Button(file_frame, text="Chọn file", command=self.browse_file)
        browse_btn.pack(side='left', padx=5)

        preview_label = ttk.Label(parent, text="Xem trước dữ liệu:")
        preview_label.pack(anchor='w', padx=20, pady=5)

        table_frame = ttk.Frame(parent)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)

        columns = ('ma_khach_hang', 'tai_khoan')
        self.verification_table = ttk.Treeview(table_frame, columns=columns, show='headings')
        self.verification_table.heading('ma_khach_hang', text='Mã khách hàng')
        self.verification_table.heading('tai_khoan', text='Tài khoản')
        self.verification_table.column('ma_khach_hang', width=150)
        self.verification_table.column('tai_khoan', width=250)
        self.verification_table.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.verification_table.yview)
        scrollbar.pack(side='right', fill='y')
        self.verification_table.configure(yscrollcommand=scrollbar.set)

    def setup_execution_tab(self, parent):
        """
        Thiết lập tab thực thi quy trình xác minh, bao gồm trạng thái, điều khiển và nhật ký.

        :param parent: Frame cha chứa tab này.
        """
        header_label = ttk.Label(parent, text="Thực thi quy trình xác minh", style='Header.TLabel')
        header_label.pack(pady=10)

        status_frame = ttk.LabelFrame(parent, text="Trạng thái")
        status_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(status_frame, text="Số tài khoản MCC đã chọn:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.mcc_count_label = ttk.Label(status_frame, text="0")
        self.mcc_count_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(status_frame, text="Số tài khoản cần xác minh:").grid(
            row=0, column=3, padx=5, pady=5, sticky='w')
        self.verification_count_label = ttk.Label(status_frame, text="0/0")
        self.verification_count_label.grid(row=0, column=4, padx=5, pady=5, sticky='e')

        ttk.Label(status_frame, text="Số luồng:").grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.thread_spinbox = ttk.Spinbox(
            status_frame,
            from_=1,
            to=100,
            width=5,
            textvariable=self.thread_count,
            state='readonly'
        )
        self.thread_spinbox.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='w')

        ttk.Label(status_frame, text="Số tài khoản đã xác minh:").grid(
            row=1, column=3, padx=5, pady=5, sticky='w')
        self.verified_count_label = ttk.Label(status_frame, text="0/0")
        self.verified_count_label.grid(row=1, column=4, padx=5, pady=5, sticky='e')

        self.login_check = ttk.Checkbutton(
            status_frame,
            text="Đã đăng nhập",
            variable=self.login_checked
        )
        self.login_check.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='w')

        ttk.Label(status_frame, text="Trạng thái:").grid(row=4, column=3, padx=5, pady=5, sticky='w')
        self.status_label = ttk.Label(status_frame, text="Chưa bắt đầu")
        self.status_label.grid(row=4, column=4, padx=5, pady=5, sticky='w')

        control_frame = ttk.Frame(parent)
        control_frame.pack(fill='x', padx=20, pady=10)

        self.start_btn = ttk.Button(control_frame, text="Bắt đầu xác minh", command=self.start_browsers)
        self.start_btn.pack(side='left', padx=5)

        self.confirm_btn = ttk.Button(control_frame, text="Xác nhận đã đăng nhập", command=self.confirm_login, state='disabled')
        self.confirm_btn.pack(side='left', padx=5)

        log_frame = ttk.LabelFrame(parent, text="Nhật ký hoạt động")
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.log_text = tk.Text(log_frame, height=10, wrap='word', state='disabled')
        self.log_text.pack(side='left', fill='both', expand=True)

        log_scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_text.yview)
        log_scrollbar.pack(side='right', fill='y')
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        progress_frame = ttk.Frame(parent)
        progress_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(progress_frame, text="Tiến độ xác minh:").pack(side='left')
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side='left', fill='x', expand=True, padx=5)
        self.progress_percent = ttk.Label(progress_frame, text="0%")
        self.progress_percent.pack(side='left')

    def update_spinbox_state(self):
        """
        Cập nhật trạng thái của spinbox số luồng dựa trên số tài khoản MCC được chọn.
        """
        if not self.account_data.empty:
            selected_count = len(self.account_data[self.account_data['Status'] == 1])
            if selected_count > 1:
                self.thread_spinbox.configure(state='disabled')
                self.thread_count.set(selected_count)
            else:
                self.thread_spinbox.configure(state='readonly')
                if selected_count == 0:
                    self.thread_count.set(1)

    def load_existing_data(self):
        """
        Tải dữ liệu tài khoản MCC từ file Account_id.csv nếu tồn tại.
        """
        if os.path.exists('Account_id.csv'):
            try:
                self.account_data = pd.read_csv('Account_id.csv')
                self.update_account_table()
                self.update_status()
                self.update_spinbox_state()
            except Exception:
                self.log(f"Không thể đọc file Account_id.csv")

    def load_existing_verification_data(self):
        """
        Tải dữ liệu xác minh từ file bcxm.csv nếu tồn tại, cập nhật bảng và trạng thái.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, 'bcxm.csv')

        if os.path.exists(template_path):
            try:
                df = pd.read_csv(template_path)
                self.verification_data = df[df['Trạng thái xác minh'] == 0]
                verified_count = len(df[df['Trạng thái xác minh'] == 1])
                self.verified_count = verified_count
                self.verified_count_label.config(text=str(verified_count))

                self.file_path_var.set(template_path)
                self.update_verification_table()
                self.update_status()
            except Exception:
                self.log(f"Không thể đọc file bcxm.csv")
                self.verification_data = None

    def check_account_name(self, name):
        """
        Kiểm tra tên tài khoản có hợp lệ (không dấu, không khoảng trắng).

        :param name: Tên tài khoản cần kiểm tra.
        :return: Tuple (bool, thông báo lỗi nếu có).
        """
        import unicodedata

        if ' ' in name:
            return False, "Tên tài khoản phải viết liền"

        normalized_name = unicodedata.normalize('NFKD', name)
        has_accents = any(unicodedata.combining(c) for c in normalized_name)
        if has_accents:
            return False, "Tên tài khoản không được chứa dấu"

        return True, ""

    def add_account(self):
        """
        Thêm tài khoản MCC mới vào danh sách sau khi kiểm tra hợp lệ.
        """
        # Lấy dữ liệu từ form nhập
        account_id = self.id_entry.get().strip()
        account_name = self.name_entry.get().strip()

        # Kiểm tra dữ liệu placeholder
        if account_id == "123-456-7890" or account_name == "Tên tài khoản viết liền không dấu":
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ ID và tên tài khoản MCC")
            return

        # Kiểm tra dữ liệu rỗng
        if not account_id or not account_name:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ ID và tên tài khoản MCC")
            return

        # Kiểm tra tính hợp lệ của tên tài khoản
        is_valid, message = self.check_account_name(account_name)
        if not is_valid:
            messagebox.showwarning("Thông báo", message)
            return

        # Kiểm tra trùng lặp ID
        if self.account_data['ID'].astype(str).str.strip().eq(str(account_id)).any():
            messagebox.showwarning("Thông báo", f"Tài khoản {account_id} đã tồn tại trong danh sách")
            return

        # Thêm tài khoản mới vào DataFrame
        new_row = pd.DataFrame({'ID': [account_id], 'Name': [account_name], 'Status': [0]})
        self.account_data = pd.concat([self.account_data, new_row], ignore_index=True)

        # Xóa dữ liệu trong form
        self.id_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')

        # Cập nhật giao diện và lưu file
        self.update_account_table()
        self.update_status()
        self.log(f"Đã thêm tài khoản MCC: {account_name} với ID: {account_id}")
        self.save_account_data()

    def remove_account(self):
        """
        Xóa các tài khoản MCC được chọn khỏi danh sách và cập nhật file.
        """
        selected_items = self.account_table.selection()
        if not selected_items:
            messagebox.showinfo("Thông báo", "Vui lòng chọn tài khoản cần xóa")
            return

        accounts_to_remove = []
        for item in selected_items:
            values = self.account_table.item(item, 'values')
            accounts_to_remove.append({
                'id': str(values[1]).strip(),
                'name': str(values[2]).strip()
            })

        confirm_message = "Bạn có chắc chắn muốn xóa các tài khoản sau không?\n\n"
        for acc in accounts_to_remove:
            confirm_message += f"- {acc['name']} (ID: {acc['id']})\n"

        if not messagebox.askyesno("Xác nhận xóa", confirm_message):
            return

        original_length = len(self.account_data)
        for acc in accounts_to_remove:
            mask = self.account_data['ID'].astype(str).str.strip() != acc['id']
            self.account_data = self.account_data[mask]
            self.log(f"Đang xóa tài khoản MCC: {acc['name']} với ID: {acc['id']}")

        removed_count = original_length - len(self.account_data)
        if removed_count > 0:
            self.save_account_data()
            self.update_account_table()
            self.update_status()
            self.log(f"Đã xóa {removed_count} tài khoản MCC")
        else:
            self.log("Không có tài khoản nào được xóa")

    def update_account_table(self):
        """
        Cập nhật bảng hiển thị danh sách tài khoản MCC trên giao diện.
        """
        try:
            self.account_table.delete(*self.account_table.get_children())

            if self.account_data.empty:
                return

            sorted_data = self.account_data.copy()
            sorted_data['ID'] = sorted_data['ID'].astype(str).str.strip()
            sorted_data['Name'] = sorted_data['Name'].astype(str).str.strip()
            sorted_data = sorted_data.sort_values(by='ID')

            for _, row in sorted_data.iterrows():
                try:
                    status = "☑" if row.get('Status', 0) == 1 else "☐"
                    self.account_table.insert('', 'end', values=(status, row['ID'], row['Name']))
                except Exception:
                    self.log(f"Lỗi khi thêm dòng {row['ID']}")

        except Exception:
            self.log(f"Lỗi khi cập nhật bảng")
            messagebox.showerror("Lỗi", f"Không thể cập nhật bảng")

        self.account_table.update()

    def browse_file(self):
        """
        Mở hộp thoại chọn file CSV, xử lý và lưu dữ liệu xác minh vào bcxm.csv.
        """
        file_path = filedialog.askopenfilename(
            title="Chọn file CSV",
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            uploaded_data = pd.read_csv(file_path, skiprows=2, encoding='utf-8')
            uploaded_data.columns = uploaded_data.columns.str.strip()

            script_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(script_dir, 'bcxm.csv')

            template_df = pd.DataFrame({
                'Mã khách hàng': uploaded_data['Mã khách hàng'],
                'Tài khoản': uploaded_data['Tài khoản'],
                'Trạng thái xác minh': [0] * len(uploaded_data)
            })
            template_df.to_csv(template_path, index=False)

            self.load_existing_verification_data()

    def load_verification_file(self, file_path):
        """
        Tải và hợp nhất dữ liệu xác minh từ file CSV được chọn vào bcxm.csv.

        :param file_path: Đường dẫn file CSV cần tải.
        :return: DataFrame chứa dữ liệu xác minh chưa hoàn thành.
        """
        try:
            uploaded_data = pd.read_csv(file_path, skiprows=2, encoding='utf-8')
            uploaded_data.columns = uploaded_data.columns.str.strip()

            script_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(script_dir, 'bcxm.csv')

            if os.path.exists(template_path):
                existing_data = pd.read_csv(template_path)
                merged_data = pd.concat([
                    existing_data,
                    pd.DataFrame({
                        'Mã khách hàng': uploaded_data['Mã khách hàng'],
                        'Tài khoản': uploaded_data['Tài khoản'],
                        'Trạng thái xác minh': [0] * len(uploaded_data)
                    })
                ]).drop_duplicates(subset=['Mã khách hàng', 'Tài khoản'], keep='first')
            else:
                merged_data = pd.DataFrame({
                    'Mã khách hàng': uploaded_data['Mã khách hàng'],
                    'Tài khoản': uploaded_data['Tài khoản'],
                    'Trạng thái xác minh': [0] * len(uploaded_data)
                })

            merged_data.to_csv(template_path, index=False)

            self.verification_data = merged_data[merged_data['Trạng thái xác minh'] == 0]
            self.update_verification_table()
            self.update_status()
            return self.verification_data

        except Exception:
            messagebox.showerror("Lỗi", f"Không thể đọc file")
            self.log(f"Lỗi khi tải file xác minh")
            return None

    def update_verification_table(self):
        """
        Cập nhật bảng hiển thị dữ liệu xác minh trên giao diện.
        """
        for item in self.verification_table.get_children():
            self.verification_table.delete(item)

        if self.verification_data is not None:
            for i, row in self.verification_data.iterrows():
                if i < 100:
                    self.verification_table.insert('', 'end', values=(row['Mã khách hàng'], row['Tài khoản']))

            if len(self.verification_data) > 100:
                self.verification_table.insert('', 'end', values=('...', f'(Còn {len(self.verification_data) - 100} dòng khác)'))

    def update_status(self):
        """
        Cập nhật các nhãn trạng thái về số lượng tài khoản MCC, xác minh, đã xác minh.
        """
        selected_mcc_count = len(self.account_data[self.account_data['Status'] == 1])
        self.mcc_count_label.config(text=str(selected_mcc_count))

        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(script_dir, 'bcxm.csv')
            if os.path.exists(template_path):
                df = pd.read_csv(template_path)
                total_accounts = len(df)
                verified_accounts = len(df[df['Trạng thái xác minh'] == 1])
                unverified_accounts = len(df[df['Trạng thái xác minh'] == 0])

                self.verification_count_label.config(
                    text=f"{unverified_accounts}/{total_accounts}")
                self.verified_count_label.config(
                    text=f"{verified_accounts}/{total_accounts}")

                # Cập nhật tiến độ dựa trên dữ liệu hiện tại
                self.update_progress(verified_accounts, total_accounts)
        except Exception:
            self.log(f"Lỗi khi cập nhật trạng thái")
            self.verification_count_label.config(text="0/0")
            self.verified_count_label.config(text="0/0")
            self.update_progress(0, 0)

    def log(self, message, color="black"):
        """
        Ghi nhật ký hoạt động lên giao diện và in ra console với màu sắc và icon.

        :param message: Nội dung nhật ký.
        :param color: Màu sắc hiển thị (red, yellow, green, black).
        """
        timestamp = time.strftime("%H:%M:%S", time.localtime())

        # Thêm icon tương ứng với loại thông báo
        icon = ""
        if color == "red":
            icon = "❌ "
        elif color == "yellow":
            icon = "⚠️ "
        elif color == "green":
            icon = "✅ "
        else:
            icon = ""

        log_message = f"[{timestamp}] {icon}{message}\n"

        self.log_text.configure(state='normal')

        # Tạo tag cho màu sắc nếu chưa có
        tag_name = f"color_{color}"
        if tag_name not in self.log_text.tag_names():
            if color == "red":
                self.log_text.tag_configure(tag_name, foreground="#D32F2F")  # Đỏ
            elif color == "yellow":
                self.log_text.tag_configure(tag_name, foreground="#F9A825")  # Vàng
            elif color == "green":
                self.log_text.tag_configure(tag_name, foreground="#388E3C")  # Xanh lá
            else:
                self.log_text.tag_configure(tag_name, foreground="black")    # Đen

        # Chèn text với màu sắc
        start_pos = self.log_text.index('end-1c')
        self.log_text.insert('end', log_message)
        end_pos = self.log_text.index('end-1c')
        self.log_text.tag_add(tag_name, start_pos, end_pos)

        self.log_text.configure(state='disabled')
        self.log_text.see('end')
        print(log_message.strip())

    def start_browsers(self):
        """
        Khởi động các luồng xác minh tài khoản con bằng Selenium, chia dữ liệu theo số luồng.
        """
        # Kiểm tra nếu đã đang chạy
        if self.is_running:
            messagebox.showinfo("Thông báo", "Quá trình đã được khởi động")
            return

        # Lấy danh sách tài khoản MCC được chọn
        selected_accounts = self.account_data[self.account_data['Status'] == 1]
        if len(selected_accounts) == 0:
            messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất một tài khoản MCC")
            return

        # Đọc file dữ liệu xác minh
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, 'bcxm.csv')

        try:
            verification_df = pd.read_csv(template_path)
            # Lọc các tài khoản chưa xác minh
            unverified_accounts = verification_df[verification_df['Trạng thái xác minh'] == 0]

            if len(unverified_accounts) == 0:
                messagebox.showinfo("Thông báo", "Tất cả tài khoản đã được xác minh")
                return

            self.verification_data = unverified_accounts
        except Exception:
            messagebox.showerror("Lỗi", f"Không thể đọc file bcxm.csv")
            return

        try:
            # Chia dữ liệu theo số luồng
            chunks = np.array_split(self.verification_data, self.thread_count.get())

            # Thiết lập trạng thái đang chạy
            self.is_running = True
            self.status_label.config(text="Đang thực hiện...")
            self.start_btn.config(state='disabled')

            # Xử lý trạng thái đăng nhập
            if not self.login_checked.get():
                self.confirm_btn.config(state='normal')
            else:
                self.confirmation_received.set()
                self.confirm_btn.config(state='disabled')

            # Chuẩn bị danh sách tài khoản cho các luồng
            self.threads = []
            list_account_id = []
            list_account_name = []

            if len(selected_accounts) == 1:
                # Một tài khoản cho nhiều luồng
                account = selected_accounts.iloc[0]
                list_account_id = [account['ID']] * self.thread_count.get()
                list_account_name = [account['Name']] * self.thread_count.get()
            else:
                # Mỗi luồng một tài khoản
                list_account_id = selected_accounts['ID'].tolist()
                list_account_name = selected_accounts['Name'].tolist()

            # Khởi tạo và chạy các luồng
            for idx, ((account_id, name_account), chunk) in enumerate(zip(
                    zip(list_account_id, list_account_name),
                    chunks)):
                thread = threading.Thread(
                    target=self.account_verification_thread,
                    args=(idx, account_id, name_account, chunk)
                )
                thread.daemon = True
                thread.start()
                self.threads.append(thread)
                time.sleep(1)  # Delay giữa các luồng

        except Exception:
            self.log(f"Lỗi khi khởi động trình duyệt")
            messagebox.showerror("Lỗi", f"Không thể khởi động trình duyệt")
            return

    def confirm_login(self):
        """
        Xác nhận đã đăng nhập Google Ads, cho phép các luồng tiếp tục thực hiện xác minh.
        """
        if not self.is_running:
            return

        self.confirmation_received.set()
        self.confirm_btn.config(state='disabled')

    def account_verification_thread(self, idx, account_id, name_account, chunk):
        """
        Luồng thực hiện xác minh danh tính cho một phần dữ liệu tài khoản con.

        :param idx: Chỉ số luồng.
        :param account_id: ID tài khoản MCC.
        :param name_account: Tên tài khoản MCC.
        :param chunk: Phần dữ liệu xác minh được giao cho luồng này.
        """
        try:
            # Thiết lập Chrome options
            options = uc.ChromeOptions()
            profile_directory = f"Profile_{idx + 1}_{name_account}"
            if not os.path.exists(profile_directory):
                os.makedirs(profile_directory)

            # Khởi tạo Chrome driver với thread-safe
            with self.driver_lock:
                options.user_data_dir = profile_directory
                try:
                    driver = uc.Chrome(options=options)
                    self.drivers.append(driver)
                except Exception:
                    self.log_from_thread(f"Không thể khởi tạo Chromedriver ở luồng {idx + 1}, vui lòng update Chrome")
                    return

            # Thiết lập vị trí và kích thước cửa sổ
            if self.secondary_monitor:
                window_width = self.secondary_monitor.width // 3
                window_height = self.secondary_monitor.height // 2
                position_x = self.secondary_monitor.x + (idx * window_width // 20) - 1600
                position_y = self.secondary_monitor.y
            else:
                screen_width = driver.execute_script("return window.screen.availWidth;")
                screen_height = driver.execute_script("return window.screen.availHeight;")
                window_width = screen_width // 3
                window_height = screen_height // 2
                position_x = idx * window_width // 20
                position_y = 0

            driver.set_window_size(window_width, window_height)
            driver.set_window_position(position_x, position_y)

            # Thiết lập zoom và mở Google Ads
            driver.execute_script("document.body.style.zoom='100%'")
            driver.get("https://ads.google.com/aw/overview")

            # Chờ xác nhận đăng nhập
            if not self.login_checked.get():
                self.log_from_thread(f"Luồng {idx + 1}: Vui lòng đăng nhập", "yellow")

            self.confirmation_received.wait()

            if not self.is_running:
                return

            # Xử lý từng tài khoản trong chunk
            for index, row in chunk.iterrows():
                if not self.is_running:
                    return

                ma_khach_hang = row['Mã khách hàng']
                name_customer = row['Tài khoản']

                # Ghi nhận thời điểm bắt đầu xử lý tài khoản
                account_start_time = time.time()

                try:
                    # Thiết lập zoom và điều hướng
                    driver.execute_script("document.body.style.zoom='50%'")
                    driver.get("https://ads.google.com/aw/overview")

                    self.log_from_thread(f"Luồng {idx + 1}: Đang tìm tài khoản MCC {account_id}...", "yellow")
                    account_id_xpath = config.get_account_id_xpath(account_id)
                    if not click.auto_click(driver, account_id_xpath, 30,
                                            log_callback=lambda msg: self._get_color_callback(idx, msg)):
                        self.log_from_thread(f"Luồng {idx + 1}: Không thể tìm thấy MCC, vui lòng kiểm tra ID {account_id}", "red")
                        continue

                    driver.execute_script("document.body.style.zoom='50%'")
                    time.sleep(5)

                    self.log_from_thread(f"Luồng {idx + 1}: Đang tìm icon mũi tên chỉ xuống...", "yellow")
                    if not click.auto_click(driver, config.arrow_drop_down_button_xpath, 30,
                                            log_callback=lambda msg: self._get_color_callback(idx, msg)):
                        self.log_from_thread(f"Luồng {idx + 1}: Không tìm thấu icon mũi tên chỉ xuống", "red")
                        continue

                    time.sleep(3)

                    self.log_from_thread(f"Luồng {idx + 1}: Đang tìm icon kính lúp...", "yellow")
                    if not click.auto_click(driver, config.search_button_xpath, 30,
                                            log_callback=lambda msg: self._get_color_callback(idx, msg)):
                        self.log_from_thread(f"Luồng {idx + 1}: Không thể tìm thấy icon kính lúp", "red")
                        continue

                    # Nhập mã khách hàng
                    ActionChains(driver).send_keys(f"{ma_khach_hang}").perform()
                    time.sleep(3)

                    try:
                        # Click vào tên khách hàng
                        self.log_from_thread(f"Luồng {idx + 1}: Đang tìm tài khoản khách hàng {name_customer}...", "yellow")
                        customer_xpath = config.get_customer_name_xpath(name_customer)
                        element = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, customer_xpath))
                        )
                        driver.execute_script("arguments[0].click();", element)
                        self.log_from_thread(f"Luồng {idx + 1}: Đã tìm thấy và click vào tài khoản {name_customer}", "green")
                    except Exception:
                        self.log_from_thread(f"Luồng {idx + 1}: Không tìm thấy tài khoản {name_customer}", "red")
                        continue

                    time.sleep(5)

                    # Truy cập mục thanh toán
                    self.log_from_thread(f"Luồng {idx + 1}: Đang tìm mục thanh toán...", "yellow")
                    if not click.auto_click(driver, config.pay_button_xpath, 30,
                                            log_callback=lambda msg: self._get_color_callback(idx, msg)):
                        self.log_from_thread(f"Luồng {idx + 1}: Không thể truy cập vào mục thanh toán", "red")
                        continue

                    # Click vào quy trình xác minh
                    self.log_from_thread(f"Luồng {idx + 1}: Đang tìm mục quy trình xác minh...", "yellow")
                    if not click.auto_click(driver, config.verification_process_button_xpath, 10,
                                            log_callback=lambda msg: self._get_color_callback(idx, msg)):
                        self.log_from_thread(f"Luồng {idx + 1}: Không thể click vào mục quy trình xác minh", "red")
                        continue

                    time.sleep(5)

                    # Xử lý các bước xác minh
                    self.log_from_thread(f"Luồng {idx + 1}: Đang kiểm tra trạng thái nhiệm vụ 1 cho tài khoản {name_customer}...", "yellow")

                    # Kiểm tra xem có nút bắt đầu nhiệm vụ 1 không
                    mission_1_available = click.auto_click(driver, config.start_mission_button_xpath, 5,
                                                           log_callback=lambda msg: self._get_color_callback(idx, msg))

                    if mission_1_available:
                        self.log_from_thread(f"Luồng {idx + 1}: Tìm thấy nhiệm vụ 1 cho tài khoản {name_customer}, đang xử lý...", "yellow")
                        time.sleep(5)

                        try:
                            WebDriverWait(driver, 20).until(
                                EC.visibility_of_element_located((By.XPATH, config.radio_group_xpath))
                            )

                            time.sleep(3)

                            # Chọn radio button đầu tiên
                            self.log_from_thread(f"Luồng {idx + 1}: Đang chọn người thanh toán...", "yellow")
                            try:
                                radio_element = WebDriverWait(driver, 15).until(
                                    EC.element_to_be_clickable((By.XPATH, config.first_radio_xpath))
                                )
                                ActionChains(driver).move_to_element(radio_element).click().perform()
                                self.log_from_thread(f"Luồng {idx + 1}: Đã chọn người thanh toán cho tài khoản {name_customer}", "green")
                            except Exception:
                                self.log_from_thread(f"Luồng {idx + 1}: Không tìm thấy lựa chọn người thanh toán", "red")
                                continue

                            time.sleep(3)

                            # Submit câu trả lời
                            try:
                                submit_element = WebDriverWait(driver, 15).until(
                                    EC.element_to_be_clickable((By.XPATH, config.submit_button_xpath))
                                )
                                ActionChains(driver).move_to_element(submit_element).click().perform()
                                self.log_from_thread(f"Luồng {idx + 1}: Đã nhấn nút \"Gửi câu trả lời\" cho tài khoản {name_customer}", "green")
                                time.sleep(3)
                            except Exception:
                                self.log_from_thread(f"Luồng {idx + 1}: Không tìm thấy nút \"Gửi câu trả lời\"", "red")
                                continue

                        except Exception:
                            self.log_from_thread(f"Luồng {idx + 1}: Popup nhiệm vụ 1 chưa hiển thị hoặc có lỗi cho tài khoản {name_customer}", "red")

                    self.log_from_thread(f"Luồng {idx + 1}: Đã hoàn tất xử lý nhiệm vụ 1 cho tài khoản {name_customer}", "green")

                    # Click nút bắt đầu xác minh
                    self.log_from_thread(f"Luồng {idx + 1}: Đang tìm nút \"Bắt đầu xác minh\" cho tài khoản {name_customer}...", "yellow")
                    verification_started = False

                    if click.auto_click(driver, config.start_mission_button_xpath_2, 10,
                                        log_callback=lambda msg: self._get_color_callback(idx, msg)):
                        self.log_from_thread(f"Luồng {idx + 1}: Đã click nút \"Bắt đầu nhiệm vụ\" cho {name_customer}", "green")
                        verification_started = True
                    else:
                        self.log_from_thread(f"Luồng {idx + 1}: Không tìm thấy nút \"Bắt đầu nhiệm vụ\", đang thử tìm nút \"Bắt đầu xác minh\"...", "red")
                        if click.auto_click(driver, config.start_verification_button_xpath, 5,
                                            log_callback=lambda msg: self._get_color_callback(idx, msg)):
                            self.log_from_thread(f"Luồng {idx + 1}: Đã click nút \"Bắt đầu xác minh\" cho {name_customer}", "green")
                            verification_started = True

                    if not verification_started:
                        # Tài khoản có thể đã được xác minh
                        self.log_from_thread(f"Luồng {idx + 1}: Tài khoản {name_customer} có thể đã được xác minh trước đó", "red")
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        template_path = os.path.join(script_dir, 'bcxm.csv')

                        # Cập nhật trạng thái đã xác minh
                        with self.file_lock:
                            try:
                                df = pd.read_csv(template_path)
                                mask = (df['Mã khách hàng'] == ma_khach_hang) & (df['Tài khoản'] == name_customer)
                                df.loc[mask, 'Trạng thái xác minh'] = 1
                                df.to_csv(template_path, index=False)
                                self.increment_verified_count()
                            except Exception:
                                self.log_from_thread(f"Luồng {idx + 1}: Không thể cập nhật trạng thái xác minh cho tài khoản {name_customer}")
                        continue

                    time.sleep(3)

                    # Tích các checkbox
                    self.log_from_thread(f"Luồng {idx + 1}: Đang tích các checkbox xác minh cho {name_customer}...", "yellow")
                    if not click.auto_click(driver, config.check_box_1_xpath, 5,
                                            log_callback=lambda msg: self._get_color_callback(idx, msg)):
                        self.log_from_thread(f"Luồng {idx + 1}: Không có checkbox 1, tiếp tục...", "yellow")

                    if not click.auto_click(driver, config.check_box_2_xpath, 5,
                                            log_callback=lambda msg: self._get_color_callback(idx, msg)):
                        self.log_from_thread(f"Luồng {idx + 1}: Không có checkbox 2, tiếp tục...", "yellow")

                    time.sleep(5)

                    # Click nút lưu và tiếp tục
                    self.log_from_thread(f"Luồng {idx + 1}: Đang tìm nút \"Lưu và tiếp tục\" cho {name_customer}...", "yellow")
                    if not click.auto_click(driver, config.save_and_continue_button_xpath, 30,
                                            log_callback=lambda msg: self._get_color_callback(idx, msg)):
                        self.log_from_thread(f"Luồng {idx + 1}: Không thể nhấn nút \"Lưu và tiếp tục\" cho {name_customer}", "red")
                        continue
                    else:
                        self.log_from_thread(f"Luồng {idx + 1}: Đã hoàn tất quy trình xác minh cho {name_customer}", "green")

                    # Cập nhật trạng thái xác minh thành công
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    template_path = os.path.join(script_dir, 'bcxm.csv')

                    with self.file_lock:
                        try:
                            df = pd.read_csv(template_path)
                            mask = (df['Mã khách hàng'] == ma_khach_hang) & (df['Tài khoản'] == name_customer)
                            df.loc[mask, 'Trạng thái xác minh'] = 1
                            df.to_csv(template_path, index=False)
                        except Exception:
                            self.log_from_thread(f"Luồng {idx + 1}: Không thể cập nhật trạng thái xác minh")

                    # Tính toán thời gian thực hiện
                    account_end_time = time.time()
                    execution_time = account_end_time - account_start_time
                    minutes = int(execution_time // 60)
                    seconds = int(execution_time % 60)

                    if minutes > 0:
                        time_str = f"{minutes} phút {seconds} giây"
                    else:
                        time_str = f"{seconds} giây"

                    self.log_from_thread(f"Luồng {idx + 1}: Đã xác minh tài khoản {name_customer} thành công (Thời gian: {time_str})", "green")
                    self.increment_verified_count()

                    if self.thread_count.get() == 1:
                        time.sleep(10)
                    else:
                        time.sleep(30)

                except Exception:
                    self.log_from_thread(f"Luồng {idx + 1}: Lỗi khi xác minh tài khoản {name_customer}", "red")
                    continue

            self.log_from_thread(f"Luồng {idx + 1}: Đã hoàn tất xác minh tất cả các tài khoản được giao", "green")

            # Kiểm tra và reset UI nếu tất cả luồng hoàn thành
            with self.driver_lock:
                self.drivers.remove(driver)
                if not self.drivers:
                    self.root.after(0, lambda: self.reset_ui_after_completion())

        except Exception as e:
            self.log_from_thread(f"Luồng {idx + 1}: Lỗi không xác định: {str(e)}", "red")

        finally:
            # Đóng driver và cleanup
            try:
                driver.quit()
                with self.driver_lock:
                    if driver in self.drivers:
                        self.drivers.remove(driver)
            except Exception:
                pass

    def log_from_thread(self, message, color="black"):
        """
        Ghi nhật ký từ luồng con, đảm bảo thread-safe.

        :param message: Nội dung nhật ký.
        :param color: Màu sắc hiển thị (red, yellow, green, black).
        """
        self.root.after(0, lambda: self.log(message, color))

    def _get_color_callback(self, idx, msg):
        """
        Xử lý callback từ click.auto_click và phân loại màu sắc dựa trên nội dung thông báo.

        :param idx: Chỉ số luồng.
        :param msg: Thông báo từ hàm auto_click.
        """
        message = f"Luồng {idx + 1}: {msg}"

        # Phân loại màu dựa trên nội dung
        if "Đã click thành công" in msg:
            self.log_from_thread(message, "green")
        elif "Đang thử lại" in msg or "đang thử lại" in msg:
            self.log_from_thread(message, "yellow")
        elif "Không thể click" in msg or "Không tìm thấy" in msg:
            self.log_from_thread(message, "red")
        else:
            self.log_from_thread(message, "black")

    def update_progress(self, verified_count, total_count):
        """
        Cập nhật tiến độ xác minh dựa trên số tài khoản đã xác minh.

        :param verified_count: Số lượng tài khoản đã xác minh.
        :param total_count: Tổng số lượng tài khoản cần xác minh.
        """
        if total_count > 0:
            progress = (verified_count / total_count) * 100
            self.root.after(0, lambda: self.update_progress_ui(progress))
        else:
            self.root.after(0, lambda: self.update_progress_ui(0))

    def update_progress_ui(self, progress):
        """
        Cập nhật giao diện tiến độ xác minh.

        :param progress: Phần trăm tiến độ.
        """
        self.progress_var.set(progress)
        self.progress_percent.config(text=f"{int(progress)}%")

        if progress >= 100:
            self.status_label.config(text="Hoàn thành")
            self.start_btn.config(state='normal')
            self.confirm_btn.config(state='disabled')
            self.is_running = False

    def save_account_data(self, retry_count=3):
        """
        Lưu dữ liệu tài khoản MCC vào file Account_id.csv, thử lại nếu gặp lỗi.

        :param retry_count: Số lần thử lưu file.
        :return: True nếu lưu thành công, False nếu thất bại.
        """
        for attempt in range(retry_count):
            try:
                # Lưu file với thread-safe
                with self.file_lock:
                    self.account_data.to_csv('Account_id.csv', index=False)
                return True
            except Exception:
                if attempt < retry_count - 1:
                    self.log(f"Lần {attempt + 1}: Không thể lưu file, đang thử lại...")
                    time.sleep(1)  # Delay trước khi thử lại
                else:
                    messagebox.showerror("Lỗi", f"Không thể lưu file sau {retry_count} lần thử")
                    self.log(f"Không thể lưu danh sách tài khoản vào file Account_id.csv")
                    return False

    def increment_verified_count(self):
        """
        Tăng số lượng tài khoản đã xác minh và cập nhật giao diện, tiến độ.
        """
        with self.verified_count_lock:
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                template_path = os.path.join(script_dir, 'bcxm.csv')
                df = pd.read_csv(template_path)
                total_accounts = len(df)
                verified_count = len(df[df['Trạng thái xác minh'] == 1])

                # Cập nhật label số lượng đã xác minh
                self.root.after(0, lambda: self.verified_count_label.config(
                    text=f"{verified_count}/{total_accounts}"))

                # Cập nhật tiến độ xác minh
                self.update_progress(verified_count, total_accounts)

            except Exception:
                self.log(f"Lỗi khi cập nhật trạng thái")

    def _on_id_entry_focus_in(self):
        """
        Xử lý sự kiện khi ô nhập ID tài khoản MCC được focus.
        """
        if self.id_entry.get() == "123-456-7890":
            self.id_entry.delete(0, 'end')
            self.id_entry.config(foreground='black')

    def _on_id_entry_focus_out(self):
        """
        Xử lý sự kiện khi ô nhập ID tài khoản MCC mất focus.
        """
        if not self.id_entry.get():
            self.id_entry.insert(0, "123-456-7890")
            self.id_entry.config(foreground='gray')

    def _on_name_entry_focus_in(self):
        """
        Xử lý sự kiện khi ô nhập tên tài khoản MCC được focus.
        """
        if self.name_entry.get() == "Tên tài khoản viết liền không dấu":
            self.name_entry.delete(0, 'end')
            self.name_entry.config(foreground='black')

    def _on_name_entry_focus_out(self):
        """
        Xử lý sự kiện khi ô nhập tên tài khoản MCC mất focus.
        """
        if not self.name_entry.get():
            self.name_entry.insert(0, "Tên tài khoản viết liền không dấu")
            self.name_entry.config(foreground='gray')

    def collapse_window(self):
        """
        Thu gọn hoặc mở rộng cửa sổ ứng dụng.
        """
        if not self.is_collapsed:
            self.root.geometry(f"{self.COLLAPSED_WIDTH}x{self.COLLAPSED_HEIGHT}")
            self.collapse_button.config(text="Mở rộng")
        else:
            self.root.geometry(f"{self.EXPANDED_WIDTH}x{self.EXPANDED_HEIGHT}")
            self.collapse_button.config(text="Thu gọn")
        self.is_collapsed = not self.is_collapsed

    def reset_ui_after_completion(self):
        """
        Reset giao diện sau khi hoàn thành xác minh.
        """
        self.is_running = False
        self.start_btn.config(state='normal')
        self.confirm_btn.config(state='disabled')
        self.status_label.config(text="Đã hoàn thành")
        self.confirmation_received.clear()


if __name__ == "__main__":
    """
    Điểm bắt đầu chương trình, khởi tạo và chạy ứng dụng Tkinter.
    """
    # Khởi tạo root window
    root = tk.Tk()
    # Tạo instance ứng dụng
    app = GoogleAdsVerificationApp(root)
    # Chạy main loop
    root.mainloop()
