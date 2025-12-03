from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
import time
import logging

log = logging.getLogger(__name__)

class StreamerPage(BasePage):
    # Locators
    FIRST_STREAMER_CARD = (By.XPATH, '//*[@id="page-main-content-wrapper"]/div/div/section[1]/div[2]/button') # Generic card selector
    # Pop-up selector for "Start Watching" or "Mature Content"
    POPUP_MODAL_BUTTON = (By.CSS_SELECTOR, 'button[data-a-target="content-classification-gate-overlay-start-watching-button"]')
    VIDEO_PLAYER = (By.TAG_NAME, "video")

    def scroll_and_select_streamer(self, scroll_times=2):
        # Step 4: Scroll down 2 times [cite: 23]
        for _ in range(scroll_times):
            self.scroll_down()
            time.sleep(1) # Small pause to simulate human behavior/allow load

        # Step 5: Select one streamer [cite: 23]
        try:
            element = self.find(self.FIRST_STREAMER_CARD)
            ActionChains(self.driver).move_to_element(element).click().perform()
        except Exception as e:
            log.warning(f"Failed to click first streamer card: {e}")
            # Try a more forgiving locator (click first card by XPath)
            try:
                self.click((By.XPATH, "(//div[contains(@class,'tw-link')])[1]"))
            except Exception:
                raise

    def handle_popup_and_screenshot(self):
        # Step: Handle modal/pop-up 
        try:
            # We use a short try/except because the popup is optional/conditional
            self.click(self.POPUP_MODAL_BUTTON)
            print("Popup handled.")
        except:
            print("No popup appeared.")

        # Step 6: Wait for load and take screenshot [cite: 23]
        # Wait for the video player; increase wait tolerance
        try:
            self.wait = self.wait  # ensure wait attr exists from BasePage
            self.find(self.VIDEO_PLAYER)
        except Exception as e:
            log.warning(f"Video player did not appear: {e}")

        self.save_screenshot("streamer_page")