arrow_drop_down_button_xpath = '//material-icon[@icon="arrow_drop_down"]//i[text()="arrow_drop_down"]'
search_button_xpath = "//div[contains(@class, 'customer-search-button')]//i[contains(@class, 'material-icon-i') and text()='search']"
pay_button_xpath = "//sidebar-panel[@id='navigation.billing']//a[contains(@class, 'title-container')]"
verification_process_button_xpath = "//sidebar-panel[@id='navigation.billing.advertiserVerificationIdentity']//a[contains(@class, 'title-container')]"


def get_account_id_xpath(account_id):
    return f"//span[text()='{account_id}']"


def get_customer_name_xpath(customer_name):
    return f"//a[contains(@class, 'customer-title') and div//div[contains(@class, 'customer-name') and text()='{customer_name}']]"


# task 1
task1_start_button_xpath = "//verification-card[.//h3[contains(text(), 'dự định chạy quảng cáo')]]//material-button[contains(@class, 'task-item-button') and .//div[text()='Bắt đầu nhiệm vụ']]"
task1_radio_group_xpath = "//material-radio-group[@role='radiogroup']"
task1_no_option_xpath = "//material-radio[contains(@class, 'noOption')]"
task1_submit_button_xpath = "//material-button[contains(@class, 'btn-yes') and contains(@class, 'highlighted') and .//div[text()='Gửi câu trả lời']]"

# task 2
task2_start_verification_button_xpath = "//material-button[contains(@class, 'action-button')]//div[text()='Bắt đầu xác minh']"
task2_start_button_xpath = "//verification-card[.//span[contains(text(), 'tổ chức')]]//material-button[contains(@class, 'task-item-button') and .//div[text()='Bắt đầu nhiệm vụ']]"
task2_organization_button_xpath = "//material-button[contains(@class, 'task-item-button') and contains(@class, 'filled-button') and contains(@aria-label, 'tổ chức')]"
task2_radio_group_xpath = "//material-radio-group[@role='radiogroup']"
task2_radio2_xpath = "(//material-ripple[@aria-hidden='true' and contains(@class, 'ripple')])[2]"
task2_radio4_xpath = "(//material-ripple[@aria-hidden='true' and contains(@class, 'ripple')])[4]"
task2_save_button_xpath = "//material-button[contains(@class, 'save-button') and @role='button']"

# task 3
task3_start_button_xpath = "//verification-card[.//span[contains(text(), 'người thanh toán')]]//material-button[contains(@class, 'task-item-button') and .//div[text()='Bắt đầu nhiệm vụ']]"
task3_payment_button_xpath = "//material-button[contains(@class, 'task-item-button') and contains(@class, 'filled-button') and contains(@aria-label, 'người thanh toán')]"
task3_radio_group_xpath = "//material-radio-group[@role='radiogroup']"
task3_first_radio_xpath = "//material-radio[contains(@class, 'radio-option')][1]"
task3_submit_button_xpath = "//material-button[contains(@class, 'filled') and .//div[text()='Gửi câu trả lời']]"

# general
verification_complete_xpath = "//h3[contains(text(), 'Bạn đã hoàn tất mọi nhiệm vụ bắt buộc')]"
