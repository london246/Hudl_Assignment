import random
import string
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def generate_random_email():
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}@testmail.com"

def wait_for_element(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))

def wait_for_url_contains(driver, partial_url, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.url_contains(partial_url))