from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class BasePage:

    def __init__(self, driver: webdriver, url=None):
        self.driver = driver
        if url:
            try:
                self.driver.get(url)
            except WebDriverException:
                self.driver.quit()

    def wait_for_element(self, by, name):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((by, name)))
        except TimeoutException:
            element = None
        return element

    def wait_for_elements(self, by, name):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((by, name)))
        except TimeoutException:
            return None
        return self.driver.find_elements(by, name)

    def wrap(self) -> bool:
        pass
