"""
Task handlers for Google Ads verification
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


def handle_task1(driver, idx, name_customer, log_callback):
    """
    Xử lý nhiệm vụ 1 (Task 1) - Câu hỏi về quảng cáo chính trị ở Liên minh Châu Âu.

    :param driver: Chrome driver instance.
    :param idx: Chỉ số luồng.
    :param name_customer: Tên tài khoản khách hàng.
    :param log_callback: Hàm callback để ghi log.
    :return: True nếu thành công, False nếu thất bại.
    """
    try:
        log_callback(f"Luồng {idx + 1}: Xử lý Task 1 cho tài khoản {name_customer}...", "yellow")

        # Tìm và click nút "Bắt đầu nhiệm vụ" cho câu hỏi về quảng cáo chính trị EU
        try:
            # Tìm nút bắt đầu nhiệm vụ trong verification card có chứa câu hỏi về EU
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, config.task1_start_button_xpath)
                )
            )
            driver.execute_script("arguments[0].click();", button)
            log_callback(f"Luồng {idx + 1}: Đã click nút 'Bắt đầu nhiệm vụ' cho Task 1", "green")
        except Exception as e:
            log_callback(f"Luồng {idx + 1}: Không tìm thấy nút bắt đầu Task 1: {str(e)}", "yellow")
            return False

        time.sleep(3)

        # Chờ popup hiện ra với câu hỏi về quảng cáo chính trị EU
        try:
            popup = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, config.task1_radio_group_xpath))
            )
            log_callback(f"Luồng {idx + 1}: Popup Task 1 đã hiện ra", "green")
        except Exception as e:
            log_callback(f"Luồng {idx + 1}: Popup Task 1 không hiện ra: {str(e)}", "red")
            return False

        time.sleep(2)

        # Chọn radio button "Không" (noOption) cho câu hỏi về quảng cáo chính trị EU
        try:
            radio = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, config.task1_no_option_xpath))
            )
            driver.execute_script("arguments[0].click();", radio)
            log_callback(f"Luồng {idx + 1}: Đã chọn 'Không' cho câu hỏi quảng cáo chính trị", "green")
        except Exception as e:
            log_callback(f"Luồng {idx + 1}: Không thể chọn radio button Task 1: {str(e)}", "red")
            return False

        time.sleep(1)

        # Nhấn nút "Gửi câu trả lời"
        try:
            submit_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, config.task1_submit_button_xpath))
            )
            driver.execute_script("arguments[0].click();", submit_button)
            log_callback(f"Luồng {idx + 1}: Đã nhấn nút 'Gửi câu trả lời' Task 1", "green")
        except Exception as e:
            log_callback(f"Luồng {idx + 1}: Không thể nhấn nút submit Task 1: {str(e)}", "yellow")

        time.sleep(3)
        log_callback(f"Luồng {idx + 1}: Task 1 hoàn thành cho tài khoản {name_customer}", "green")
        return True

    except Exception as e:
        log_callback(f"Luồng {idx + 1}: Lỗi khi xử lý Task 1: {str(e)}", "red")
        return False


def handle_task2(driver, idx, name_customer, log_callback):
    """
    Xử lý nhiệm vụ 2 (Task 2) - Xác minh tổ chức.

    :param driver: Chrome driver instance.
    :param idx: Chỉ số luồng.
    :param name_customer: Tên tài khoản khách hàng.
    :param log_callback: Hàm callback để ghi log.
    :return: True nếu thành công, False nếu thất bại.
    """
    try:
        log_callback(f"Luồng {idx + 1}: Xử lý Task 2 cho tài khoản {name_customer}...", "yellow")

        # Tìm và click nút bắt đầu Task 2
        task2_started = False

        # Thử click nút "Bắt đầu xác minh" (trường hợp cũ)
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, config.task2_start_verification_button_xpath))
            )
            driver.execute_script("arguments[0].click();", button)
            log_callback(f"Luồng {idx + 1}: Đã click nút 'Bắt đầu xác minh' cho Task 2", "green")
            task2_started = True
        except Exception:
            # Thử click nút "tổ chức" (trường hợp cũ)
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, config.task2_organization_button_xpath))
                )
                driver.execute_script("arguments[0].click();", button)
                log_callback(f"Luồng {idx + 1}: Đã click nút 'tổ chức' cho Task 2", "green")
                task2_started = True
            except Exception:
                # Thử click nút "Bắt đầu nhiệm vụ" cho Task 2 (trường hợp mới)
                try:
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, config.task2_start_button_xpath))
                    )
                    driver.execute_script("arguments[0].click();", button)
                    log_callback(f"Luồng {idx + 1}: Đã click nút 'Bắt đầu nhiệm vụ' cho Task 2", "green")
                    task2_started = True
                except Exception:
                    log_callback(f"Luồng {idx + 1}: Không tìm thấy nút bắt đầu Task 2", "yellow")
                    return False

        if not task2_started:
            return False

        time.sleep(3)

        # Chọn radio button thứ 2
        try:
            radio2 = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, config.task2_radio2_xpath))
            )
            driver.execute_script("arguments[0].click();", radio2)
            log_callback(f"Luồng {idx + 1}: Đã chọn radio button thứ 2", "green")
        except Exception as e:
            log_callback(f"Luồng {idx + 1}: Không thể chọn radio button thứ 2: {str(e)}", "red")
            return False

        # Chọn radio button thứ 4
        try:
            radio4 = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, config.task2_radio4_xpath))
            )
            driver.execute_script("arguments[0].click();", radio4)
            log_callback(f"Luồng {idx + 1}: Đã chọn radio button thứ 4", "green")
        except Exception as e:
            log_callback(f"Luồng {idx + 1}: Không thể chọn radio button thứ 4: {str(e)}", "red")
            return False

        time.sleep(2)

        # Nhấn nút lưu
        try:
            save_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, config.task2_save_button_xpath))
            )
            driver.execute_script("arguments[0].click();", save_button)
            log_callback(f"Luồng {idx + 1}: Đã nhấn nút lưu Task 2", "green")
        except Exception as e:
            log_callback(f"Luồng {idx + 1}: Không thể nhấn nút lưu Task 2: {str(e)}", "red")
            return False

        time.sleep(3)
        log_callback(f"Luồng {idx + 1}: Task 2 hoàn thành cho tài khoản {name_customer}", "green")
        return True

    except Exception as e:
        log_callback(f"Luồng {idx + 1}: Lỗi khi xử lý Task 2: {str(e)}", "red")
        return False


def handle_task3(driver, idx, name_customer, log_callback):
    """
    Xử lý nhiệm vụ 3 (Task 3) - Xác minh người thanh toán.

    :param driver: Chrome driver instance.
    :param idx: Chỉ số luồng.
    :param name_customer: Tên tài khoản khách hàng.
    :param log_callback: Hàm callback để ghi log.
    :return: True nếu thành công, False nếu thất bại.
    """
    try:
        log_callback(f"Luồng {idx + 1}: Xử lý Task 3 cho tài khoản {name_customer}...", "yellow")

        # Click nút bắt đầu Task 3
        task3_started = False

        # Thử click nút "người thanh toán" (trường hợp cũ)
        try:
            button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, config.task3_payment_button_xpath))
            )
            driver.execute_script("arguments[0].click();", button)
            log_callback(f"Luồng {idx + 1}: Đã click nút 'người thanh toán' cho Task 3", "green")
            task3_started = True
        except Exception:
            # Thử click nút "Bắt đầu nhiệm vụ" cho Task 3 (trường hợp mới)
            try:
                button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, config.task3_start_button_xpath))
                )
                driver.execute_script("arguments[0].click();", button)
                log_callback(f"Luồng {idx + 1}: Đã click nút 'Bắt đầu nhiệm vụ' cho Task 3", "green")
                task3_started = True
            except Exception as e:
                log_callback(f"Luồng {idx + 1}: Không tìm thấy nút bắt đầu Task 3: {str(e)}", "yellow")
                return False

        if not task3_started:
            return False

        time.sleep(3)

        # Chờ popup hiện ra
        try:
            popup = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, config.task3_radio_group_xpath))
            )
            log_callback(f"Luồng {idx + 1}: Popup Task 3 đã hiện ra", "green")
        except Exception as e:
            log_callback(f"Luồng {idx + 1}: Popup Task 3 không hiện ra: {str(e)}", "red")
            return False

        time.sleep(1)

        # Chọn radio button đầu tiên
        try:
            radio = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, config.task3_first_radio_xpath))
            )
            driver.execute_script("arguments[0].click();", radio)
            log_callback(f"Luồng {idx + 1}: Đã chọn radio button đầu tiên trong Task 3", "green")
        except Exception as e:
            log_callback(f"Luồng {idx + 1}: Không thể chọn radio button Task 3: {str(e)}", "red")
            return False

        time.sleep(2)

        # Nhấn nút "Gửi câu trả lời"
        try:
            submit_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, config.task3_submit_button_xpath))
            )
            driver.execute_script("arguments[0].click();", submit_button)
            log_callback(f"Luồng {idx + 1}: Đã nhấn nút 'Gửi câu trả lời' Task 3", "green")
        except Exception as e:
            log_callback(f"Luồng {idx + 1}: Không thể nhấn nút 'Gửi câu trả lời' Task 3: {str(e)}", "red")
            return False

        time.sleep(3)
        log_callback(f"Luồng {idx + 1}: Task 3 hoàn thành cho tài khoản {name_customer}", "green")
        return True

    except Exception as e:
        log_callback(f"Luồng {idx + 1}: Lỗi khi xử lý Task 3: {str(e)}", "red")
        return False


def check_and_execute_tasks(driver, idx, name_customer, log_callback):
    """
    Kiểm tra và thực hiện các nhiệm vụ xác minh.

    :param driver: Chrome driver instance.
    :param idx: Chỉ số luồng.
    :param name_customer: Tên tài khoản khách hàng.
    :param log_callback: Hàm callback để ghi log.
    :return: True nếu có ít nhất một nhiệm vụ được thực hiện, False nếu không có nhiệm vụ nào.
    """
    try:
        log_callback(f"Luồng {idx + 1}: Đang kiểm tra các nhiệm vụ xác minh cho {name_customer}...", "yellow")

        # Kiểm tra xem tài khoản đã được xác minh trước đó chưa
        try:
            completed_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, config.verification_complete_xpath))
            )
            log_callback(f"Luồng {idx + 1}: Tài khoản {name_customer} đã được xác minh trước đó rồi", "green")
            return True  # Trả về True vì tài khoản đã được xác minh
        except Exception:
            # Không tìm thấy thông báo hoàn thành, tiếp tục kiểm tra các task
            pass

        # Kiểm tra tất cả task có sẵn ngay từ đầu
        initial_tasks = get_all_available_tasks(driver)
        if initial_tasks:
            log_callback(f"Luồng {idx + 1}: Tìm thấy {len(initial_tasks)} task có sẵn: {', '.join(initial_tasks)}", "blue")

            # Xử lý các trường hợp đặc biệt
            if len(initial_tasks) == 1:
                log_callback(f"Luồng {idx + 1}: Chỉ có 1 nhiệm vụ cần xử lý", "blue")
            elif len(initial_tasks) == 2:
                log_callback(f"Luồng {idx + 1}: Có 2 nhiệm vụ cần xử lý", "blue")
            elif len(initial_tasks) == 3:
                log_callback(f"Luồng {idx + 1}: Có đủ 3 nhiệm vụ cần xử lý", "blue")
        else:
            log_callback(f"Luồng {idx + 1}: Không tìm thấy task nào có sẵn - có thể đã hoàn thành", "yellow")

        tasks_completed = 0
        max_iterations = 5  # Tối đa 5 lần lặp để tránh vòng lặp vô hạn
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            tasks_found_in_this_iteration = 0

            log_callback(f"Luồng {idx + 1}: Kiểm tra lần thứ {iteration}...", "blue")

            # Kiểm tra và thực hiện Task 1
            try:
                if check_task1_available(driver):
                    log_callback(f"Luồng {idx + 1}: Tìm thấy Task 1, đang xử lý...", "blue")
                    if handle_task1(driver, idx, name_customer, log_callback):
                        tasks_completed += 1
                        tasks_found_in_this_iteration += 1
                        # Không log "Task 1 hoàn thành" ở đây vì handle_task1() đã log rồi
            except Exception as e:
                log_callback(f"Luồng {idx + 1}: Lỗi khi xử lý Task 1: {str(e)}", "red")

            # Kiểm tra và thực hiện Task 2
            try:
                if check_task2_available(driver):
                    log_callback(f"Luồng {idx + 1}: Tìm thấy Task 2, đang xử lý...", "blue")
                    if handle_task2(driver, idx, name_customer, log_callback):
                        tasks_completed += 1
                        tasks_found_in_this_iteration += 1
                        # Không log "Task 2 hoàn thành" ở đây vì handle_task2() đã log rồi
            except Exception as e:
                log_callback(f"Luồng {idx + 1}: Lỗi khi xử lý Task 2: {str(e)}", "red")

            # Kiểm tra và thực hiện Task 3
            try:
                if check_task3_available(driver):
                    log_callback(f"Luồng {idx + 1}: Tìm thấy Task 3, đang xử lý...", "blue")
                    if handle_task3(driver, idx, name_customer, log_callback):
                        tasks_completed += 1
                        tasks_found_in_this_iteration += 1
                        # Không log "Task 3 hoàn thành" ở đây vì handle_task3() đã log rồi
            except Exception as e:
                log_callback(f"Luồng {idx + 1}: Lỗi khi xử lý Task 3: {str(e)}", "red")

            # Kiểm tra lại xem tài khoản đã được xác minh hoàn toàn chưa
            if is_verification_complete(driver):
                log_callback(f"Luồng {idx + 1}: Tài khoản {name_customer} đã được xác minh hoàn toàn", "green")
                return True

            # Nếu không tìm thấy task nào trong lần lặp này, dừng lại
            if tasks_found_in_this_iteration == 0:
                log_callback(f"Luồng {idx + 1}: Không tìm thấy task nào trong lần kiểm tra thứ {iteration}", "yellow")
                break

            # Chờ một chút trước khi kiểm tra lại
            time.sleep(2)

        # Kiểm tra kết quả cuối cùng
        final_check_tasks = get_all_available_tasks(driver)

        if tasks_completed == 0:
            if final_check_tasks:
                log_callback(f"Luồng {idx + 1}: Không thể hoàn thành các task còn lại: {', '.join(final_check_tasks)}", "red")
                return False
            else:
                log_callback(f"Luồng {idx + 1}: Tài khoản {name_customer} đã có thể được xác minh trước đó rồi", "yellow")
                return False
        else:
            if final_check_tasks:
                log_callback(f"Luồng {idx + 1}: Đã hoàn thành {tasks_completed} nhiệm vụ, còn lại: {', '.join(final_check_tasks)}", "orange")
            else:
                log_callback(f"Luồng {idx + 1}: Đã hoàn thành tất cả {tasks_completed} nhiệm vụ cho {name_customer}", "green")
            return True

    except Exception as e:
        log_callback(f"Luồng {idx + 1}: Lỗi khi kiểm tra nhiệm vụ: {str(e)}", "red")
        return False


def check_task2_available(driver):
    """
    Kiểm tra xem Task 2 có khả dụng không (nhiệm vụ về tổ chức).

    :param driver: Chrome driver instance.
    :return: True nếu Task 2 khả dụng, False nếu không.
    """
    try:
        button1 = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, config.task2_start_verification_button_xpath))
        )
        return True
    except Exception:
        try:
            button2 = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, config.task2_organization_button_xpath))
            )
            return True
        except Exception:
            try:
                button3 = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(
                        (By.XPATH, config.task2_start_button_xpath))
                )
                return True
            except Exception:
                return False


def check_task3_available(driver):
    """
    Kiểm tra xem Task 3 có khả dụng không (nhiệm vụ về người thanh toán).

    :param driver: Chrome driver instance.
    :return: True nếu Task 3 khả dụng, False nếu không.
    """
    try:
        button1 = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, config.task3_payment_button_xpath))
        )
        return True
    except Exception:
        try:
            button2 = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, config.task3_start_button_xpath))
            )
            return True
        except Exception:
            return False


def check_task1_available(driver):
    """
    Kiểm tra xem Task 1 có khả dụng không (câu hỏi về quảng cáo chính trị EU).

    :param driver: Chrome driver instance.
    :return: True nếu Task 1 khả dụng, False nếu không.
    """
    try:
        button = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, config.task1_start_button_xpath))
        )
        return True
    except Exception:
        return False


def get_all_available_tasks(driver):
    """
    Kiểm tra tất cả các task có sẵn trên trang.

    :param driver: Chrome driver instance.
    :return: List các task có sẵn.
    """
    available_tasks = []

    # Kiểm tra Task 1
    if check_task1_available(driver):
        available_tasks.append("Task 1 (EU political ads)")

    # Kiểm tra Task 2
    if check_task2_available(driver):
        available_tasks.append("Task 2 (Organization)")

    # Kiểm tra Task 3
    if check_task3_available(driver):
        available_tasks.append("Task 3 (Payment info)")

    return available_tasks


def is_verification_complete(driver):
    """
    Kiểm tra xem quá trình xác minh đã hoàn thành chưa.

    :param driver: Chrome driver instance.
    :return: True nếu đã hoàn thành, False nếu chưa.
    """
    try:
        # Kiểm tra thông báo hoàn thành
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, config.verification_complete_xpath))
        )
        return True
    except Exception:
        # Kiểm tra xem còn task nào không
        remaining_tasks = get_all_available_tasks(driver)
        return len(remaining_tasks) == 0
