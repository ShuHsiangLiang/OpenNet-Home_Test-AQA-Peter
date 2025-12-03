from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
import logging
from selenium.common.exceptions import TimeoutException

log = logging.getLogger(__name__)

class HomePage(BasePage):
    # Locators (Note: These are examples; actual Twitch selectors change frequently)
    # Explicitly load the home feed (not redirected to a streamer channel)
    URL = "https://m.twitch.tv/home"
    # Primary locators (may change depending on mobile version)
    SEARCH_ICON = (By.CSS_SELECTOR, 'a[href="/directory"]')
    SEARCH_ICON_ALT = (By.CSS_SELECTOR, 'button[aria-label="Search"]')
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[type="search"]')
    SEARCH_INPUT_ALT = (By.XPATH, '//input[contains(@placeholder, "Search") or contains(@aria-label, "Search")]')

    def load(self):
        self.driver.get(self.URL)
        # Wait for page to load and stabilize before proceeding
        import time
        time.sleep(2)

    def search_for_streamer(self, keyword):
        # Log current page info for debugging
        try:
            log.info(f"Current URL before search: {self.driver.current_url}")
            log.info(f"Page title: {self.driver.title}")
        except Exception:
            pass

        # On Twitch mobile, search is usually triggered via a button/link
        # Try multiple fallback locators in order
        search_found = False
        
        # Attempt 1: Primary CSS selector for search icon
        try:
            log.info("Attempting SEARCH_ICON CSS selector...")
            self.click(self.SEARCH_ICON)
            search_found = True
        except Exception as e:
            log.info(f"SEARCH_ICON failed: {e}")
        
        # Attempt 2: Alternative CSS selector (button with aria-label)
        if not search_found:
            try:
                log.info("Attempting SEARCH_ICON_ALT...")
                self.click(self.SEARCH_ICON_ALT)
                search_found = True
            except Exception as e:
                log.info(f"SEARCH_ICON_ALT failed: {e}")
        
        # Attempt 3: Generic XPath looking for search-like elements
        if not search_found:
            try:
                log.info("Attempting generic XPath for search...")
                generic_xpath = (By.XPATH, "//*[contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'search') or @href='/search' or @data-a-target='search-button']")
                self.click(generic_xpath)
                search_found = True
            except Exception as e:
                log.info(f"Generic XPath failed: {e}")
        
        if not search_found:
            raise RuntimeError("Could not locate search element using any available locator")
        
        # Now try to find and fill the search input
        try:
            log.info(f"Sending search keyword: {keyword}")
            self.send_keys(self.SEARCH_INPUT, keyword)
            self.find(self.SEARCH_INPUT).send_keys(Keys.ENTER)
        except Exception as e1:
            log.info(f"Primary SEARCH_INPUT failed: {e1}, trying alternate...")
            try:
                self.send_keys(self.SEARCH_INPUT_ALT, keyword)
                self.find(self.SEARCH_INPUT_ALT).send_keys(Keys.ENTER)
            except Exception as e2:
                log.info(f"Alternate SEARCH_INPUT failed: {e2}, trying generic fallback...")
                search_input_generic = (By.XPATH, "//input[contains(@placeholder, 'search') or contains(@placeholder, 'Search') or @type='search']")
                self.send_keys(search_input_generic, keyword)
                self.find(search_input_generic).send_keys(Keys.ENTER)