"""
Event handler functions for UI
"""

from data import browse_and_load_file


def setup_event_handlers(app_instance):
    """
    Thiết lập các event handlers cho ứng dụng.

    :param app_instance: Instance của ứng dụng chính.
    """
    # Thiết lập event handlers cho các entry fields
    app_instance.id_entry.bind('<FocusIn>', lambda e: app_instance._on_id_entry_focus_in())
    app_instance.id_entry.bind('<FocusOut>', lambda e: app_instance._on_id_entry_focus_out())
    app_instance.name_entry.bind('<FocusIn>', lambda e: app_instance._on_name_entry_focus_in())
    app_instance.name_entry.bind('<FocusOut>', lambda e: app_instance._on_name_entry_focus_out())


def on_id_entry_focus_in(id_entry):
    """
    Xử lý sự kiện khi ô nhập ID tài khoản MCC được focus.

    :param id_entry: Entry widget cho ID tài khoản.
    """
    if id_entry.get() == "123-456-7890":
        id_entry.delete(0, 'end')
        id_entry.config(foreground='black')


def on_id_entry_focus_out(id_entry):
    """
    Xử lý sự kiện khi ô nhập ID tài khoản MCC mất focus.

    :param id_entry: Entry widget cho ID tài khoản.
    """
    if not id_entry.get():
        id_entry.insert(0, "123-456-7890")
        id_entry.config(foreground='gray')


def on_name_entry_focus_in(name_entry):
    """
    Xử lý sự kiện khi ô nhập tên tài khoản MCC được focus.

    :param name_entry: Entry widget cho tên tài khoản.
    """
    if name_entry.get() == "Tên tài khoản viết liền không dấu":
        name_entry.delete(0, 'end')
        name_entry.config(foreground='black')


def on_name_entry_focus_out(name_entry):
    """
    Xử lý sự kiện khi ô nhập tên tài khoản MCC mất focus.

    :param name_entry: Entry widget cho tên tài khoản.
    """
    if not name_entry.get():
        name_entry.insert(0, "Tên tài khoản viết liền không dấu")
        name_entry.config(foreground='gray')


def browse_file_handler(app_instance):
    """
    Xử lý sự kiện chọn file CSV.

    :param app_instance: Instance của ứng dụng chính.
    """
    file_path = browse_and_load_file()
    if file_path:
        app_instance.file_path_var.set(file_path)
        app_instance.load_existing_verification_data()
