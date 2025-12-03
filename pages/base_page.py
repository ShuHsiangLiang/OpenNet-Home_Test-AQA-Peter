import os
import time
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver, default_timeout: int = 30):
        self.driver = driver
        # Increase default wait to 30s to be more tolerant of slow loads
        self.wait = WebDriverWait(driver, default_timeout)
        self._timeout = default_timeout

    def find(self, locator):
        log.info(f"Waiting for presence of element: {locator}")
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        log.info(f"Waiting for element to be clickable: {locator}")
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def send_keys(self, locator, text):
        log.info(f"Waiting for element to be visible for send_keys: {locator}")
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def scroll_down(self, pixels=500):
        """Helper to scroll down as requested in the test steps."""
        log.info(f"Scrolling down by {pixels} pixels")
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")

    def save_screenshot(self, name):
        """Saves screenshot to the screenshots folder."""
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        path = os.path.join(screenshots_dir, f"{name}.png")
        try:
            self.driver.save_screenshot(path)
            log.info(f"Saved screenshot: {path}")
        except Exception as e:
            log.warning(f"Failed to save screenshot {path}: {e}")