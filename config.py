arrow_drop_down_button_xpath = '//material-icon[@icon="arrow_drop_down"]//i[text()="arrow_drop_down"]'
search_button_xpath = "//div[contains(@class, 'customer-search-button')]//i[contains(@class, 'material-icon-i') and text()='search']"
pay_button_xpath = "//sidebar-panel[@id='navigation.billing']//a[contains(@class, 'title-container')]"
verification_process_button_xpath = "//sidebar-panel[@id='navigation.billing.advertiserVerificationIdentity']//a[contains(@class, 'title-container')]"

start_mission_button_xpath = "//material-button[contains(@class, 'task-item-button') and contains(@class, 'filled-button') and contains(@aria-label, 'người thanh toán')]"
radio_group_xpath = "//material-radio-group[@role='radiogroup']"
first_radio_xpath = "//material-radio[contains(@class, 'radio-option')][1]"
submit_button_xpath = "//material-button[contains(@class, 'btn-yes') and .//div[text()='Gửi câu trả lời']]"

start_mission_button_xpath_2 = "//material-button[contains(@class, 'task-item-button') and contains(@class, 'filled-button') and contains(@aria-label, 'tổ chức')]"
start_verification_button_xpath = "//material-button[contains(@class, 'action-button')]//div[text()='Bắt đầu xác minh']"
save_and_continue_button_xpath = "//material-button[contains(@class, 'save-button') and @role='button']"

check_box_1_xpath = "(//material-ripple[@aria-hidden='true' and contains(@class, 'ripple')])[2]"
check_box_2_xpath = "(//material-ripple[@aria-hidden='true' and contains(@class, 'ripple')])[4]"


def get_account_id_xpath(account_id):
    return f"//span[text()='{account_id}']"


def get_customer_name_xpath(customer_name):
    return f"//a[contains(@class, 'customer-title') and div//div[contains(@class, 'customer-name') and text()='{customer_name}']]"
