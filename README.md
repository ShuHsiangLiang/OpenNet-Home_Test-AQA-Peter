# Twitch WAP Automation Framework

This repository contains an automated test suite for the Twitch Mobile (WAP) website. It is designed using **Python**, **Selenium**, and **pytest**, implementing the **Page Object Model (POM)** design pattern to ensure scalability and maintainability.

## 📋 Project Overview

[cite_start]The goal of this project is to automate a specific user flow on the Twitch mobile website to verify search functionality and stream selection[cite: 15, 17].

## 📂 Project Structure

twitch_automation/
├── pages/                  # Page Object classes
│   ├── base_page.py        # Common methods (click, wait, scroll)
│   ├── home_page.py        # Twitch Home page actions
│   └── streamer_page.py    # Streamer page actions & modal handling
├── tests/                  # Test scripts
│   └── test_twitch_wap.py  # Main test scenario
├── screenshots/            # Output folder for test screenshots
├── conftest.py             # Pytest configuration & WebDriver setup
└── requirements.txt        # Project dependencies

**Key Features:**
* [cite_start]**Mobile Emulation:** Uses Google Chrome's mobile emulation to simulate an "iPhone X" device[cite: 21].
* **Page Object Model:** Separates test logic from page-specific selectors and actions.
* [cite_start]**Robust Handling:** Includes logic to handle conditional pop-ups (e.g., "Start Watching" modal)[cite: 25].
* **Reporting:** Automatically saves screenshots upon reaching the target streamer page.

## 🛠 Prerequisites

* Python 3.8+
* Google Chrome Browser

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd twitch_automation
    ```

2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(See [requirements.txt](requirements.txt) for the full list of packages)*[cite: 35].

## 🏃‍♂️ How to Run the Tests

To execute the test suite, run the following command in your terminal:

```bash
pytest

📸 Test Execution Demo
(Below is the GIF showing the test running locally)