from selenium.webdriver.common.by import By

class LoginPage:
    EMAIL_INPUT = (By.ID, "username")
    CONTINUE_BTN = (By.XPATH, "//button[@name='action']")
    ERROR_EMAIL_REQUIRED = "error-cs-email-required"
    ERROR_EMAIL_INVALID = "error-cs-email-invalid"
    ERROR_EMAIL_NOT_FOUND = "error-cs-email-not-found"

    def __init__(self, driver):
        self.driver = driver

    def is_loaded(self):
        return "identity.hudl.com/u/login/identifier" in self.driver.current_url

    def enter_email(self, email):
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

    def click_continue(self):
        self.driver.find_element(*self.CONTINUE_BTN).click()

    def get_error(self, error_id):
        return self.driver.find_element(By.ID, error_id).text