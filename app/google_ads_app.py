"""
Main Google Ads Verification Application class
"""

from tkinter import ttk, messagebox
import pandas as pd

# Import modules
from .app_initializer import initialize_app
from .thread_manager import start_verification_threads
from data import load_account_data, save_account_data, load_verification_data, browse_and_load_file
from ui.table_managers import update_account_table, update_verification_table
from ui.status_updater import update_status_display, update_progress_display
from ui.tab_setup import setup_account_tab, setup_verification_tab, setup_execution_tab
from ui.event_handlers import on_id_entry_focus_in, on_id_entry_focus_out, on_name_entry_focus_in, on_name_entry_focus_out
from utils import check_account_name, log_with_timestamp


class GoogleAdsVerificationApp:
    EXPANDED_WIDTH = 800
    EXPANDED_HEIGHT = 530
    COLLAPSED_WIDTH = 590
    COLLAPSED_HEIGHT = 280

    def __init__(self, root):
        """
        Khởi tạo ứng dụng, thiết lập giao diện, trạng thái ban đầu và tải dữ liệu nếu có.

        :param root: Đối tượng Tkinter root window.
        """
        # Khởi tạo ứng dụng
        self.variables, self.style, self.secondary_monitor, self.monitors, self.widgets = initialize_app(root)

        # Gán các biến từ variables dict
        self.root = root
        self.drivers = self.variables['drivers']
        self.threads = self.variables['threads']
        self.driver_lock = self.variables['driver_lock']
        self.file_lock = self.variables['file_lock']
        self.confirmation_received = self.variables['confirmation_received']
        self.is_running = self.variables['is_running']
        self.account_data = self.variables['account_data']
        self.verification_data = self.variables['verification_data']
        self.thread_count = self.variables['thread_count']
        self.login_checked = self.variables['login_checked']
        self.verified_count = self.variables['verified_count']
        self.verified_count_lock = self.variables['verified_count_lock']
        self.is_collapsed = self.variables['is_collapsed']

        # Tạo các widget giao diện
        self.create_widgets()
        self.create_collapse_button()

        # Tải dữ liệu có sẵn từ file
        self.load_existing_data()
        # Load verification data after UI is created
        self.load_existing_verification_data()

        # Hiển thị thông báo chào mừng
        self.log("Chào mừng bạn đến với tool xác minh danh tính Google Ads! (´▽`ʃ♡ƪ)")
        self.log("Made by: Phuc TranHuwu ( •̀ ω •́ )✧")
        self.log("Vui lòng thêm MCC và tải lên file báo cáo xác minh danh tính để bắt đầu.")

    def create_widgets(self):
        """Tạo các widget giao diện."""
        notebook, execution_frame, account_frame, verification_frame = self.widgets

        setup_account_tab(account_frame, self)
        setup_verification_tab(verification_frame, self)
        setup_execution_tab(execution_frame, self)

    def create_collapse_button(self):
        """Tạo nút thu gọn cửa sổ."""
        self.collapse_button = ttk.Button(self.root, text="Thu gọn", command=self.collapse_window)
        self.collapse_button.place(relx=1.0, y=0, anchor='ne')

    def load_existing_data(self):
        """Tải dữ liệu tài khoản MCC từ file Account_id.csv nếu tồn tại."""
        self.account_data = load_account_data()
        self.update_account_table()
        self.update_status()
        self.update_spinbox_state()

    def load_existing_verification_data(self):
        """Tải dữ liệu xác minh từ file bcxm.csv nếu tồn tại."""
        verification_data, verified_count, total_count = load_verification_data()
        if verification_data is not None:
            self.verification_data = verification_data
            self.verified_count = verified_count
            # Chỉ cập nhật label nếu đã được tạo
            if hasattr(self, 'verified_count_label'):
                self.verified_count_label.config(text=str(verified_count))
            self.update_verification_table()
            self.update_status()

    def add_account(self):
        """Thêm tài khoản MCC mới vào danh sách sau khi kiểm tra hợp lệ."""
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
        is_valid, message = check_account_name(account_name)
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
        """Xóa các tài khoản MCC được chọn khỏi danh sách và cập nhật file."""
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

    def start_browsers(self):
        """Khởi động các luồng xác minh tài khoản con."""
        # Kiểm tra nếu đã đang chạy
        if self.is_running:
            messagebox.showinfo("Thông báo", "Quá trình đã được khởi động")
            return

        # Kiểm tra nếu không có tài khoản được chọn
        selected_accounts = self.account_data[self.account_data['Status'] == 1]
        if len(selected_accounts) == 0:
            messagebox.showwarning("Thông báo", "Vui lòng chọn ít nhất một tài khoản MCC")
            return

        # Kiểm tra file xác minh
        try:
            verification_df = pd.read_csv('bcxm.csv')
            unverified_accounts = verification_df[verification_df['Trạng thái xác minh'] == 0]

            if len(unverified_accounts) == 0:
                messagebox.showinfo("Thông báo", "Tất cả tài khoản đã được xác minh")
                return

            self.verification_data = unverified_accounts
        except Exception:
            messagebox.showerror("Lỗi", f"Không thể đọc file bcxm.csv")
            return

        # Khởi động các luồng
        if start_verification_threads(self):
            pass  # Đã khởi động thành công
        else:
            messagebox.showerror("Lỗi", f"Không thể khởi động trình duyệt")

    def confirm_login(self):
        """Xác nhận đã đăng nhập Google Ads."""
        if not self.is_running:
            return

        self.confirmation_received.set()
        self.confirm_btn.config(state='disabled')

    def log(self, message, color="black"):
        """Ghi nhật ký hoạt động lên giao diện."""
        log_message = log_with_timestamp(message, color)

        self.log_text.configure(state='normal')

        # Tạo tag cho màu sắc nếu chưa có
        tag_name = f"color_{color}"
        if tag_name not in self.log_text.tag_names():
            if color == "red":
                self.log_text.tag_configure(tag_name, foreground="#D32F2F")
            elif color == "yellow":
                self.log_text.tag_configure(tag_name, foreground="#F9A825")
            elif color == "green":
                self.log_text.tag_configure(tag_name, foreground="#388E3C")
            elif color == "blue":
                self.log_text.tag_configure(tag_name, foreground="#1976D2")
            elif color == "orange":
                self.log_text.tag_configure(tag_name, foreground="#F57C00")
            else:
                self.log_text.tag_configure(tag_name, foreground="black")

        # Chèn text với màu sắc
        start_pos = self.log_text.index('end-1c')
        self.log_text.insert('end', log_message + "\n")
        end_pos = self.log_text.index('end-1c')
        self.log_text.tag_add(tag_name, start_pos, end_pos)

        self.log_text.configure(state='disabled')
        self.log_text.see('end')
        print(log_message)

    def log_from_thread(self, message, color="black"):
        """Ghi nhật ký từ luồng con, đảm bảo thread-safe."""
        self.root.after(0, lambda: self.log(message, color))

    def _get_color_callback(self, idx, msg):
        """Xử lý callback từ click.auto_click và task handlers, phân loại màu sắc."""
        # Không thêm prefix vì msg đã có "Luồng {idx + 1}:" rồi
        message = msg

        # Xử lý các message từ click.auto_click
        if "Đã click thành công" in msg:
            self.log_from_thread(message, "green")
        elif "Đang thử lại" in msg or "đang thử lại" in msg:
            self.log_from_thread(message, "yellow")
        elif "Không thể click" in msg or "Không tìm thấy" in msg:
            self.log_from_thread(message, "red")

        # Xử lý các message từ task handlers
        elif any(keyword in msg for keyword in ["hoàn thành", "hoàn tất", "đã được xác minh"]):
            self.log_from_thread(message, "green")
        elif any(keyword in msg for keyword in ["đang xử lý", "đang kiểm tra", "Lần kiểm tra", "Tìm thấy"]):
            self.log_from_thread(message, "blue")
        elif any(keyword in msg for keyword in ["Lỗi", "lỗi", "không thể", "thất bại"]):
            self.log_from_thread(message, "red")
        elif any(keyword in msg for keyword in ["đã có thể được xác minh trước đó", "Không tìm thấy task"]):
            self.log_from_thread(message, "yellow")
        elif any(keyword in msg for keyword in ["còn lại", "chưa hoàn thành"]):
            self.log_from_thread(message, "orange")
        else:
            self.log_from_thread(message, "black")

    def save_account_data(self, retry_count=3):
        """Lưu dữ liệu tài khoản MCC vào file Account_id.csv."""
        return save_account_data(self.account_data, retry_count)

    def update_account_table(self):
        """Cập nhật bảng hiển thị danh sách tài khoản MCC trên giao diện."""
        if hasattr(self, 'account_table'):
            update_account_table(self.account_table, self.account_data)

    def update_verification_table(self):
        """Cập nhật bảng hiển thị dữ liệu xác minh trên giao diện."""
        if hasattr(self, 'verification_table'):
            update_verification_table(self.verification_table, self.verification_data)

    def update_status(self):
        """Cập nhật các nhãn trạng thái về số lượng tài khoản."""
        # Chỉ cập nhật nếu các label đã được tạo
        if hasattr(self, 'mcc_count_label') and hasattr(self, 'verification_count_label') and hasattr(self, 'verified_count_label'):
            update_status_display(self.mcc_count_label, self.verification_count_label,
                                  self.verified_count_label, self.account_data)

    def update_spinbox_state(self):
        """Cập nhật trạng thái của spinbox số luồng."""
        if hasattr(self, 'thread_spinbox') and not self.account_data.empty:
            selected_count = len(self.account_data[self.account_data['Status'] == 1])
            if selected_count > 1:
                self.thread_spinbox.configure(state='disabled')
                self.thread_count.set(selected_count)
            else:
                self.thread_spinbox.configure(state='readonly')
                if selected_count == 0:
                    self.thread_count.set(1)

    def increment_verified_count(self):
        """Tăng số lượng tài khoản đã xác minh và cập nhật giao diện."""
        with self.verified_count_lock:
            try:
                df = pd.read_csv('bcxm.csv')
                total_accounts = len(df)
                verified_count = len(df[df['Trạng thái xác minh'] == 1])

                # Cập nhật label số lượng đã xác minh
                self.root.after(0, lambda: self.verified_count_label.config(
                    text=f"{verified_count}/{total_accounts}"))

                # Cập nhật tiến độ xác minh
                self.update_progress(verified_count, total_accounts)

            except Exception:
                self.log(f"Lỗi khi cập nhật trạng thái")

    def update_progress(self, verified_count, total_count):
        """Cập nhật tiến độ xác minh dựa trên số tài khoản đã xác minh."""
        if total_count > 0:
            progress = (verified_count / total_count) * 100
            self.root.after(0, lambda: self.update_progress_ui(progress))
        else:
            self.root.after(0, lambda: self.update_progress_ui(0))

    def update_progress_ui(self, progress):
        """Cập nhật giao diện tiến độ xác minh."""
        update_progress_display(self.progress_var, self.progress_percent,
                                self.status_label, self.start_btn, self.confirm_btn,
                                int(progress), 100)

        if progress >= 100:
            self.status_label.config(text="Hoàn thành")
            self.start_btn.config(state='normal')
            self.confirm_btn.config(state='disabled')
            self.is_running = False

    def collapse_window(self):
        """Thu gọn hoặc mở rộng cửa sổ ứng dụng."""
        if not self.is_collapsed:
            self.root.geometry(f"{self.COLLAPSED_WIDTH}x{self.COLLAPSED_HEIGHT}")
            self.collapse_button.config(text="Mở rộng")
        else:
            self.root.geometry(f"{self.EXPANDED_WIDTH}x{self.EXPANDED_HEIGHT}")
            self.collapse_button.config(text="Thu gọn")
        self.is_collapsed = not self.is_collapsed

    def reset_ui_after_completion(self):
        """Reset giao diện sau khi hoàn thành xác minh."""
        self.is_running = False
        self.start_btn.config(state='normal')
        self.confirm_btn.config(state='disabled')
        self.status_label.config(text="Đã hoàn thành")
        self.confirmation_received.clear()

    def _on_id_entry_focus_in(self):
        """Xử lý sự kiện khi ô nhập ID tài khoản MCC được focus."""
        on_id_entry_focus_in(self.id_entry)

    def _on_id_entry_focus_out(self):
        """Xử lý sự kiện khi ô nhập ID tài khoản MCC mất focus."""
        on_id_entry_focus_out(self.id_entry)

    def _on_name_entry_focus_in(self):
        """Xử lý sự kiện khi ô nhập tên tài khoản MCC được focus."""
        on_name_entry_focus_in(self.name_entry)

    def _on_name_entry_focus_out(self):
        """Xử lý sự kiện khi ô nhập tên tài khoản MCC mất focus."""
        on_name_entry_focus_out(self.name_entry)

    def browse_file(self):
        """Xử lý sự kiện chọn file CSV."""
        browse_and_load_file()
        self.load_existing_verification_data()
