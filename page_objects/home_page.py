from selenium.webdriver.common.by import By

class HomePage:
    ACCEPT_COOKIES = (By.ID, "onetrust-accept-btn-handler")
    LOGIN_BTN = (By.XPATH, "//a[@data-qa-id='login-select']")
    HUDL_LOGIN = (By.XPATH, "//span[@class='subnavitem__label' and text()='Hudl']")

    def __init__(self, driver):
        self.driver = driver

    def accept_cookies(self):
        try:
            self.driver.find_element(*self.ACCEPT_COOKIES).click()
        except:
            pass

    def go_to_login(self):
        self.driver.find_element(*self.LOGIN_BTN).click()
        self.driver.find_element(*self.HUDL_LOGIN).click()