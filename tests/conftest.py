import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.db import Database


@pytest.fixture(params=['mysql', 'postgresql'])
def db_and_url(request):
    if request.param == 'mysql':
        db_config = {
            'host': 'localhost',
            'user': 'app',
            'password': 'pass',
            'database': 'app',
            'port': 3306
        }
        db_type = 'mysql'
        app_url = "http://localhost:8080"
    else:
        db_config = {
            'host': 'localhost',
            'user': 'app',
            'password': 'pass',
            'database': 'app',
            'port': 5432
        }
        db_type = 'postgresql'
        app_url = "http://localhost:8081"

    db = Database(db_type, db_config)
    db.connect()
    db.clear_all()
    yield db, app_url
    db.connection.close()


@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)