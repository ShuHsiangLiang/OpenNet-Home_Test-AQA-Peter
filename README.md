# Twitch Mobile Web (WAP) Automation Test Suite

A comprehensive Selenium-based automation testing framework for the Twitch mobile website, supporting both **Chrome mobile emulation** and **real Android devices/emulators** via Appium.

## 🎯 Overview

This project automates the complete user flow on Twitch mobile:
1. Navigate to Twitch home
2. Search for a specific streamer/category (e.g., "StarCraft II")
3. Scroll through results
4. Select and open a streamer channel
5. Handle modal popups if present
6. Capture final state screenshot

**Technology Stack:** Python 3.9+, Selenium, Pytest, Appium, Page Object Model (POM)

## Demo

![Automation Demo](demo_video.gif)

---

## 📁 Project Structure

```
.
├── pages/
│   ├── base_page.py           # Base class with common wait/click/scroll methods
│   ├── home_page.py           # Twitch home page object (search functionality)
│   └── streamer_page.py       # Streamer page object (scroll, select, popup handling)
├── tests/
│   └── test_twitch_wap.py     # Main test case
├── scripts/
│   └── download_chromedriver.py # Helper to auto-download matching Chromedriver
├── conftest.py                # Pytest configuration & WebDriver fixture
├── start_appium.cmd           # Helper batch file to launch Appium
├── requirements.txt           # Python dependencies
├── QUICKSTART.md              # Step-by-step setup guide
├── ANDROID_SETUP.md           # Android Emulator & Appium guide
└── screenshots/               # Test artifacts (screenshots, HTML, metadata)
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+**
- **Node.js** (for Appium)
- **Android SDK** (for Android testing)
- **Android Emulator** or real Android device

### Installation

1. **Clone the repository:**
   ```cmd
   git clone https://github.com/ShuHsiangLiang/OpenNet-Home_Test-AQA-Peter
   cd OpenNet-Home_Test-AQA-Peter
   ```

2. **Create virtual environment:**
   ```cmd
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   npm install -g appium appium-doctor
   ```

4. **Install Appium driver:**
   ```cmd
   appium driver install uiautomator2
   ```

---

## ▶️ Running Tests

### Option 1: Chrome Mobile Emulation (Default)
Fastest option, runs locally without emulator/Appium:

```cmd
pytest
```

### Option 2: Android Emulator (via Appium)
Runs on a real Android emulator with Chrome:

**Step 1:** Download matching Chromedriver
```cmd
python scripts/download_chromedriver.py --major 142
```

**Step 2:** Start Android Emulator & Appium server
```cmd
start_appium.cmd
```

**Step 3:** Run tests in another terminal
```cmd
pytest --android -v
```

---

## 📊 Test Results & Artifacts

When tests run, artifacts are automatically captured in `screenshots/`:
- **`.png`** — Screenshot of final page state
- **`.html`** — Full page source for inspection
- **`.txt`** — URL and page title metadata

---

## 🔧 Configuration

### Modify Test Behavior
- **Timeout**: Edit `pages/base_page.py` → `default_timeout` (default: 30s)
- **Device Name**: Edit `conftest.py` → `device_name` (default: "emulator-5554")
- **Search Keyword**: Edit `tests/test_twitch_wap.py` → `search_for_streamer("StarCraft II")`

### Android Emulator Configuration
- **Device**: Pixel 4, API 30+ recommended
- **Chrome Version**: Should match 142+ (auto-handled via Chromedriver download)
- **Environment Variables**: Set in `start_appium.cmd` or system PATH

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** — Complete step-by-step guide for Android testing
- **[ANDROID_SETUP.md](ANDROID_SETUP.md)** — Detailed Android SDK, Appium, and Chromedriver setup
- **[requirements.txt](requirements.txt)** — Python package versions

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: pytest` | Run `pip install -r requirements.txt` |
| `appium not found` | Install globally: `npm install -g appium` |
| `No Chromedriver for Chrome 142` | Run `python scripts/download_chromedriver.py --major 142` |
| Emulator not connecting | Verify with `adb devices` and check `conftest.py` device_name |
| Timeout waiting for element | Check `screenshots/` for captured HTML and inspect selectors |

---

## 💡 Key Features

✅ **Dual Mode:** Chrome emulation (local) or Android Emulator (real device)  
✅ **Robust Wait Handling:** 30-second default timeout with intelligent fallbacks  
✅ **Auto Artifact Capture:** Screenshots, page source, and metadata on test failure  
✅ **Logging:** Detailed logs for each action (click, wait, scroll, send_keys)  
✅ **Modal Handling:** Automatically detects and closes Twitch popups  
✅ **Fallback Locators:** Multiple selector strategies to handle UI variations  

---

## 📝 License

This project is for testing purposes.

---

## 👤 Author

**Peter Liang** — Automation QA Engineer

Repository: [OpenNet-Home_Test-AQA-Peter](https://github.com/ShuHsiangLiang/OpenNet-Home_Test-AQA-Peter)
