# XPath selectors cho các phần tử giao diện Google Ads
# Các XPath này được sử dụng để xác định và tương tác với các phần tử trong giao diện

# Button và điều hướng
arrow_drop_down_button_xpath = '//material-icon[@icon="arrow_drop_down"]//i[text()="arrow_drop_down"]'
search_button_xpath = "//*[@aria-label='Tìm kiếm khách hàng']"
pay_button_xpath = "//sidebar-panel[@id='navigation.billing']//a[@title='Thanh toán']"
verification_process_button_xpath = "//navigation-drawer-item//div[text()='Quy trình xác minh nhà quảng cáo']"

# Các nút trong quy trình xác minh
start_mission_button_xpath = "//material-button[contains(@class, 'task-item-button')]//div[text()='Bắt đầu nhiệm vụ']"
start_verification_button_xpath = "//material-button[contains(@class, 'action-button')]//div[text()='Bắt đầu xác minh']"
save_and_continue_button_xpath = "//material-button[contains(@class, 'save-button') and @role='button']//div[contains(@class, 'content') and text()='Lưu và tiếp tục']"

# Checkbox trong form xác minh
check_box_1_xpath = "(//material-ripple[@aria-hidden='true' and contains(@class, 'ripple')])[2]"
check_box_2_xpath = "(//material-ripple[@aria-hidden='true' and contains(@class, 'ripple')])[4]"

# XPath động (được tạo dựa trên dữ liệu đầu vào)


def get_account_id_xpath(account_id):
    """Tạo XPath để chọn ID tài khoản cụ thể"""
    return f"//span[text()='{account_id}']"


def get_customer_name_xpath(customer_name):
    """Tạo XPath để chọn khách hàng theo tên cụ thể"""
    return f"//a[contains(@class, 'customer-title') and div//div[contains(@class, 'customer-name') and text()='{customer_name}']]"
