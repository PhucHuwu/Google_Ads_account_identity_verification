from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import logging

logger = logging.getLogger(__name__)


def auto_click(driver, xpath, time, retries=1):
    for _ in range(retries):
        try:
            button = WebDriverWait(driver, time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()
            return True
        except Exception:
            try:
                button = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                button.click()
                return True
            except Exception:
                pass

        try:
            button = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))
            driver.execute_script("arguments[0].click();", button)
            return True
        except Exception:
            pass
    return False
