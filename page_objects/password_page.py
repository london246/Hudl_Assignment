from selenium.webdriver.common.by import By

class PasswordPage:
    PASSWORD_INPUT = (By.ID, "password")
    CONTINUE_BTN = (By.XPATH, "//button[text()='Continue']")
    ERROR_PASSWORD_REQUIRED = "error-cs-password-required"
    ERROR_PASSWORD_INCORRECT = "error-element-password"
    EDIT_EMAIL_LINK = (By.LINK_TEXT, "Edit")
    TOGGLE_PASSWORD_BUTTON = (By.CSS_SELECTOR, "button[role='switch'][data-action='toggle']")

    def __init__(self, driver):
        self.driver = driver

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_continue(self):
        self.driver.find_element(*self.CONTINUE_BTN).click()

    def get_error(self, error_id):
        return self.driver.find_element(By.ID, error_id).text

    def click_edit_email(self):
        self.driver.find_element(*self.EDIT_EMAIL_LINK).click()

    def toggle_password_visibility(self):
        self.driver.find_element(*self.TOGGLE_PASSWORD_BUTTON).click()

    def get_password_input_type(self):
        return self.driver.find_element(*self.PASSWORD_INPUT).get_attribute("type")
