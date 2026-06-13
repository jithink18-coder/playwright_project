# Playwright Functional Test Suite

Automated functional test suite for [Rahul Shetty Academy Client App](https://rahulshettyacademy.com/client/#/auth/login), built using Playwright and Pytest.

## Overview

This project covers **5 functional test scenarios** for the application, validating key user flows and ensuring application stability through automated UI testing.

## Tech Stack

- Python
- Playwright (Sync API)
- Pytest
- pytest-html (for HTML reporting)

## Prerequisites

- Python 3.x installed
- Virtual environment (recommended)

## Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd playwright_project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
USERID=your-login-username
PASSWORD=your-login-password
```

These credentials are used to log in to the application during test execution.

> **Note:** Do not commit your `.env` file. It is excluded via `.gitignore`.

## Running Tests

Run all tests:
```bash
pytest
```

Run in headed mode:
```bash
pytest --headed
```

## Reports & Artifacts

| Artifact | Location | Details |
|---|---|---|
| **Logs** | Console / log output | Captures execution flow and debug information |
| **HTML Report** | `report.html` | Test results report including **failure screenshots** |
| **Screenshots** | `screenshots/` | Captured automatically on test failure |
| **Traces** | `traces/` | Generated **only on test failure**, useful for debugging via Playwright Trace Viewer |

### Viewing a Trace

```bash
playwright show-trace traces/<trace-file>.zip
```

### Generating the HTML Report

```bash
pytest --html=report.html --self-contained-html
```

## Project Structure

```
playwright_project/
├── tests/
│   ├── test_scenario_1.py
│   ├── test_scenario_2.py
│   ├── test_scenario_3.py
│   ├── test_scenario_4.py
│   └── test_scenario_5.py
├── conftest.py
├── traces/
├── screenshots/
├── .env
├── requirements.txt
└── README.md
```

## Notes

- Each test runs in an isolated browser context for test independence.
- Failure artifacts (screenshots and traces) help in debugging failed test runs without re-execution.