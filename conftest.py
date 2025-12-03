import pytest
import os
from pathlib import Path
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options

# Set ANDROID_HOME if not already set
if not os.getenv("ANDROID_HOME"):
    android_sdk_path = str(Path.home() / "AppData" / "Local" / "Android" / "Sdk")
    if os.path.exists(android_sdk_path):
        os.environ["ANDROID_HOME"] = android_sdk_path
        # Also add platform-tools to PATH
        platform_tools = os.path.join(android_sdk_path, "platform-tools")
        if platform_tools not in os.environ.get("PATH", ""):
            os.environ["PATH"] = f"{platform_tools};{os.environ.get('PATH', '')}"

@pytest.fixture(scope="function")
def driver(request):
    """
    Initializes WebDriver based on the platform.
    Use --android flag to run tests on Android Emulator, otherwise uses Chrome mobile emulation.
    
    Example:
        pytest --android              # Run on Android Emulator
        pytest                        # Run with Chrome mobile emulation
    """
    use_android = request.config.getoption("--android", default=False)
    
    if use_android:
        _driver = _get_android_driver()
    else:
        _driver = _get_chrome_driver()
    
    yield _driver
    
    _driver.quit()

def _get_chrome_driver():
    """
    Initializes Chrome driver with Mobile Emulation (iPhone X).
    """
    mobile_emulation = { "deviceName": "iPhone X" }
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument("--headless")  # Optional: Run headless for CI/CD
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    
    return driver

def _get_android_driver():
    """
    Initializes Appium driver for Android Emulator.
    
    Prerequisites:
        - Android SDK installed and ANDROID_HOME set
        - Android Emulator running (or connect via AVD)
        - Appium Server running (typically on http://127.0.0.1:4723)
    
    Capabilities:
        - Uses Chrome browser within Android
        - Targets the running emulator
    """
    appium_server_url = "http://127.0.0.1:4723"
    
    # Get Android SDK path
    android_home = os.getenv("ANDROID_HOME")
    if not android_home:
        android_home = str(Path.home() / "AppData" / "Local" / "Android" / "Sdk")
    
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "emulator-5554"  # Default emulator; change if needed
    options.browser_name = "Chrome"
    options.w3c = True

    # Explicitly set SDK root for Appium
    options.set_capability("androidSdkPath", android_home)

    # Chromedriver handling: Appium needs a chromedriver that matches the Chrome
    # version on the emulator. You can either provide a single executable via
    # CHROMEDRIVER_PATH (env) or place multiple chromedriver binaries inside
    # a directory and set CHROMEDRIVER_DIR (env). If neither is provided,
    # Appium will try to find a suitable chromedriver but may fail.
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
    chromedriver_dir = os.getenv("CHROMEDRIVER_DIR")
    # sensible default: a folder under the user's home
    default_dir = os.path.join(str(Path.home()), "chromedrivers")

    if chromedriver_path and os.path.exists(chromedriver_path):
        options.set_capability("chromedriverExecutable", chromedriver_path)
    elif chromedriver_dir and os.path.isdir(chromedriver_dir):
        options.set_capability("chromedriverExecutableDir", chromedriver_dir)
    elif os.path.isdir(default_dir):
        options.set_capability("chromedriverExecutableDir", default_dir)

    driver = appium_webdriver.Remote(appium_server_url, options=options)
    driver.implicitly_wait(10)
    
    return driver

def pytest_addoption(parser):
    """Adds custom command-line option for Android testing."""
    parser.addoption(
        "--android",
        action="store_true",
        default=False,
        help="Run tests on Android Emulator using Appium"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only care about the actual test call phase
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
        if driver:
            try:
                screenshots_dir = Path("screenshots")
                screenshots_dir.mkdir(parents=True, exist_ok=True)

                nodeid = item.nodeid.replace("::", "__").replace("/", "_")
                ts = int(time.time())
                png = screenshots_dir / f"{nodeid}_{ts}.png"
                html = screenshots_dir / f"{nodeid}_{ts}.html"

                # save screenshot
                try:
                    driver.save_screenshot(str(png))
                except Exception:
                    pass

                # save page source
                try:
                    with open(html, "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                except Exception:
                    pass

                # save simple metadata (url + title)
                try:
                    meta = screenshots_dir / f"{nodeid}_{ts}.txt"
                    with open(meta, "w", encoding="utf-8") as mf:
                        try:
                            mf.write(f"current_url: {driver.current_url}\n")
                        except Exception:
                            mf.write("current_url: <unavailable>\n")
                        try:
                            mf.write(f"title: {driver.title}\n")
                        except Exception:
                            mf.write("title: <unavailable>\n")
                except Exception:
                    pass
            except Exception:
                # never fail the test reporting hook
                pass