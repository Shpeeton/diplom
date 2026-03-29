from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MainPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.base_url)
        return self

    def buy(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'button_size_m') and not(contains(@class, 'button_view_extra'))]"))).click()
        from pages.payment_page import PaymentPage
        return PaymentPage(self.driver)

    def credit(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'button_view_extra')]"))).click()
        from pages.payment_page import PaymentPage
        return PaymentPage(self.driver)