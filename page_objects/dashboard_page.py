from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    DISPLAY_NAME = (By.CSS_SELECTOR, ".hui-globaluseritem__display-name")
    EMAIL_ELEMENT = (By.CLASS_NAME, "hui-globaluseritem__email")
    LOGOUT_LINK = (By.XPATH, "//a[@data-qa-id='webnav-usermenu-logout']")

    def __init__(self, driver):
        self.driver = driver

    def get_user_email(self):
        hover_target = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.DISPLAY_NAME)
        )
        ActionChains(self.driver).move_to_element(hover_target).perform()
        email_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.EMAIL_ELEMENT)
        )
        return email_elem.text

    def logout(self):
        ActionChains(self.driver).move_to_element(
            self.driver.find_element(*self.DISPLAY_NAME)
        ).perform()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LOGOUT_LINK)
        ).click()