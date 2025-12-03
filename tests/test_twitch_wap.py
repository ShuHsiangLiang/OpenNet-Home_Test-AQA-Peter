from pages.home_page import HomePage
from pages.streamer_page import StreamerPage

def test_twitch_mobile_search(driver):
    """
    Test Case: Twitch WAP Search and Screenshot
    Steps cover[cite: 22, 23]:
    1. Go to Twitch
    2. Click search
    3. Input StarCraft II
    4. Scroll down 2 times
    5. Select streamer
    6. Handle modal and screenshot
    """
    # Initialize Page Objects
    home = HomePage(driver)
    streamer_page = StreamerPage(driver)

    # Execution
    home.load()
    home.search_for_streamer("StarCraft II")
    
    streamer_page.scroll_and_select_streamer(scroll_times=2)
    streamer_page.handle_popup_and_screenshot()
    
    # Validation (Implicitly handled by find() assertions in Page Objects)
    assert "twitch.tv" in driver.current_url