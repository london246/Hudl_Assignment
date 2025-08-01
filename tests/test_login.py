import pytest
import os
from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException
import allure

from page_objects.home_page import HomePage
from page_objects.login_page import LoginPage
from page_objects.password_page import PasswordPage
from page_objects.dashboard_page import DashboardPage
from utils.helpers import generate_random_email, wait_for_element, wait_for_url_contains

# Test credentials
load_dotenv()
EMAIL = os.getenv("HUDL_EMAIL")
PASSWORD = os.getenv("HUDL_PASSWORD")
WRONG_PASSWORD = "invalidPassword123"

#URL paths and expected redirects
URL_DASHBOARD_HOME = "/home"
URL_AFTER_LOGOUT = "hudl.com/en"
LOGIN_LINK_TEXT = "Log in"

# Input types for toggle assertions
PASSWORD_INPUT_TYPE_HIDDEN = "password"
PASSWORD_INPUT_TYPE_VISIBLE = "text"

# Expected UI messages
MSG_EMAIL_REQUIRED = "Enter an email address"
MSG_EMAIL_INVALID = "Enter a valid email."
MSG_EMAIL_NOT_FOUND = "We couldn't find an account with that email address"
MSG_PASSWORD_REQUIRED = "Enter your password"
MSG_LOGIN_FAILED_GENERIC = "Incorrect username or password"
MSG_LOGIN_FAILED_WITH_REGISTERED_EMAIL = "Your email or password is incorrect"
MSG_PASSWORD_HIDDEN_DEFAULT = "Password should be hidden by default"
MSG_PASSWORD_VISIBLE_AFTER_TOGGLE = "Password should be visible after toggle"


@pytest.fixture
def go_to_login(driver):
    driver.get("https://www.hudl.com")
    home = HomePage(driver)
    home.accept_cookies()
    home.go_to_login()
    login_page = LoginPage(driver)
    assert login_page.is_loaded()
    return login_page

@pytest.mark.parametrize("email,expected_error", [
    ("", MSG_EMAIL_REQUIRED),
    ("invalid123$%&@input", MSG_EMAIL_INVALID),
    (" spacing test@gmail.cz ", MSG_EMAIL_INVALID),
    ("INVALID@INPUT",MSG_EMAIL_INVALID)
],ids=[
        "empty_input",
        "special_chars",
        "whitespace_wrapped_email",
        "uppercase_invalid"
    ])
@allure.feature("Login")
@allure.story("Verifying error messages for missing or invalid email input")
def test_email_validation(go_to_login, email, expected_error):
    go_to_login.enter_email(email)
    go_to_login.click_continue()
    if not email:
        assert expected_error in go_to_login.get_error(LoginPage.ERROR_EMAIL_REQUIRED)
    else:
        assert expected_error in go_to_login.get_error(LoginPage.ERROR_EMAIL_INVALID)

@allure.feature("Login")
@allure.story("Verifying error message for unknown email address")
def test_unregistered_email(driver, go_to_login):
    login = go_to_login
    password = PasswordPage(driver)
    unregistered_email = generate_random_email()
    login.enter_email(unregistered_email)
    login.click_continue()
    try:
        wait_for_element(driver, PasswordPage.PASSWORD_INPUT)
        password.click_continue()
        assert MSG_PASSWORD_REQUIRED in password.get_error(PasswordPage.ERROR_PASSWORD_REQUIRED)
    except TimeoutException:
        assert MSG_EMAIL_NOT_FOUND in login.get_error(LoginPage.ERROR_EMAIL_NOT_FOUND)

@allure.feature("Login")
@allure.story("Verifying error message for login with unknown email and wrong password")
def test_wrong_password_unregistered_email(driver, go_to_login):
    login = go_to_login
    password = PasswordPage(driver)
    unregistered_email = generate_random_email()
    login.enter_email(unregistered_email)
    login.click_continue()
    wait_for_element(driver, PasswordPage.PASSWORD_INPUT)
    password.enter_password(WRONG_PASSWORD)
    password.click_continue()
    assert MSG_LOGIN_FAILED_GENERIC in password.get_error(PasswordPage.ERROR_PASSWORD_INCORRECT)

@allure.feature("Login")
@allure.story("Verifying the toggle password visibility using show/hide button")
def test_password_visibility_toggle(driver, go_to_login):
    login = go_to_login
    password_page = PasswordPage(driver)

    unregistered_email = generate_random_email()
    login.enter_email(unregistered_email)
    login.click_continue()
    wait_for_element(driver, PasswordPage.PASSWORD_INPUT)
    password_page.enter_password(WRONG_PASSWORD)

    assert password_page.get_password_input_type() == PASSWORD_INPUT_TYPE_HIDDEN , MSG_PASSWORD_HIDDEN_DEFAULT

    password_page.toggle_password_visibility()
    assert password_page.get_password_input_type() == PASSWORD_INPUT_TYPE_VISIBLE , MSG_PASSWORD_VISIBLE_AFTER_TOGGLE

    password_page.toggle_password_visibility()
    assert password_page.get_password_input_type() == PASSWORD_INPUT_TYPE_HIDDEN , MSG_PASSWORD_HIDDEN_DEFAULT

@allure.feature("Login")
@allure.story("Verifying login error message after editing unknown email to valid one and entering incorrect password")
def test_edit_email_to_registered_one_and_provide_wrong_password(driver, go_to_login):
    login = go_to_login
    password = PasswordPage(driver)
    unregistered_email = generate_random_email()
    login.enter_email(unregistered_email)
    login.click_continue()
    wait_for_element(driver, PasswordPage.EDIT_EMAIL_LINK)
    password.click_edit_email()
    wait_for_element(driver, LoginPage.EMAIL_INPUT)
    login.enter_email(EMAIL)
    login.click_continue()
    password.enter_password(WRONG_PASSWORD)
    password.click_continue()
    assert MSG_LOGIN_FAILED_WITH_REGISTERED_EMAIL in password.get_error(PasswordPage.ERROR_PASSWORD_INCORRECT)

@allure.feature("Login")
@allure.story("Successful login with valid credentials")
def test_valid_login(driver, go_to_login):
    login = go_to_login
    password = PasswordPage(driver)
    dashboard = DashboardPage(driver)
    login.enter_email(EMAIL)
    login.click_continue()
    password.enter_password(PASSWORD)
    password.click_continue()
    wait_for_url_contains(driver, URL_DASHBOARD_HOME)
    assert URL_DASHBOARD_HOME in driver.current_url
    assert dashboard.get_user_email() == EMAIL

@allure.feature("Login")
@allure.story("Successful logout after login")
def test_logout_after_login(driver, go_to_login):
    login = go_to_login
    password = PasswordPage(driver)
    dashboard = DashboardPage(driver)
    login.enter_email(EMAIL)
    login.click_continue()
    password.enter_password(PASSWORD)
    password.click_continue()
    wait_for_url_contains(driver, URL_DASHBOARD_HOME)
    dashboard.logout()
    wait_for_url_contains(driver, URL_AFTER_LOGOUT)
    assert LOGIN_LINK_TEXT in driver.page_source
