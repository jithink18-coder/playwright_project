Playwright Pytest POM sample

Setup

1. Create and activate a virtualenv (optional but recommended):

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
python -m playwright install
```

Run tests

```powershell
pytest -q --browsername={firefox/chromium/webkit} -n 2 --headed(optional)
```

Notes

- Tests use the Page Object Model (POM) in `pages/`.
- Tests expect `pytest-playwright` (provides the `page` fixture).