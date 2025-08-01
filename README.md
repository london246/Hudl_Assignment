# Hudl Login Automation Suite
Automated UI test suite for validating login functionality built using Python, Selenium, and Pytest.

## Setup Instructions

### Install Dependencies

```bash
  pip install -r requirements.txt
```

Or manually:

```bash
  pip install selenium pytest pytest-rerunfailures python-dotenv webdriver-manager allure-pytest
```

### 2. Setup `.env`

Create a `.env` file in the root directory:

```env
HUDL_EMAIL=your_valid_email
HUDL_PASSWORD=your_valid_password
```
Note: Created a sample .env.example file for reference and added more details in that file

---

###  Prerequisites ###

Make sure Allure CLI is installed:

#### For macOS: #####
```bash
  brew install allure
```
---

##  Running Tests

### Run all tests:

```bash
  pytest
```

##  Run Specific Test file
```bash
pytest tests/test_login.py
```
## Run specific test case 
```bash
pytest -k "test_valid_login"
```

### Run with Allure report:

```bash
# Run tests (Allure results auto-saved based on pytest.ini)
pytest
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

Clean old test results before running again
```bash
rm -rf reports/allure-results reports/allure-report
```
#### Note: Once Allure Report is Open click on `features by stories`

## Compatible with Chrome and Firefox

*  use `--browser firefox`

---
