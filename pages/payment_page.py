from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class PaymentPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def fill_card(self, number):
        self.driver.find_element(By.CSS_SELECTOR, "[placeholder='0000 0000 0000 0000']").send_keys(number)
        return self

    def fill_month(self, month):
        self.driver.find_element(By.CSS_SELECTOR, "[placeholder='08']").send_keys(month)
        return self

    def fill_year(self, year):
        self.driver.find_element(By.CSS_SELECTOR, "[placeholder='22']").send_keys(year)
        return self

    def fill_owner(self, owner):
        owner_label = self.driver.find_element(By.XPATH, "//span[@class='input__top' and text()='Владелец']")
        input_box = owner_label.find_element(By.XPATH, "./following-sibling::span[@class='input__box']")
        input_field = input_box.find_element(By.TAG_NAME, "input")
        input_field.send_keys(owner)
        return self

    def fill_cvc(self, cvc):
        self.driver.find_element(By.CSS_SELECTOR, "[placeholder='999']").send_keys(cvc)
        return self

    def submit(self):
        button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#root > div > form > fieldset > div:nth-child(4) > button")))
        button.click()
        time.sleep(11)
        return self

    def success(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".notification_status_ok")))
            return True
        except:
            return False

    def error(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".notification_status_error")))
            return True
        except:
            return False

    def get_field_error(self, field_name):
        try:
            if field_name == "card":
                field_element = self.driver.find_element(By.CSS_SELECTOR, "[placeholder='0000 0000 0000 0000']")
            elif field_name == "month":
                field_element = self.driver.find_element(By.CSS_SELECTOR, "[placeholder='08']")
            elif field_name == "year":
                field_element = self.driver.find_element(By.CSS_SELECTOR, "[placeholder='22']")
            elif field_name == "owner":
                field_element = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Владелец')]/following-sibling::span//input")
            elif field_name == "cvc":
                field_element = self.driver.find_element(By.CSS_SELECTOR, "[placeholder='999']")
            else:
                return ""

            error_elements = field_element.find_elements(By.XPATH, "./ancestor::div[contains(@class, 'form-field')]//span[@class='input__sub']")
            if error_elements:
                return error_elements[0].text
            return ""
        except:
            return ""