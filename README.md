# Automated UI Tests — 21vek.by

End-to-end UI test suite for [21vek.by](https://www.21vek.by) built with **Playwright + pytest**.

## Stack

| Tool | Purpose |
|---|---|
| [Playwright](https://playwright.dev/python/) | Browser automation |
| [pytest](https://pytest.org) | Test runner |
| [pytest-html](https://pytest-html.readthedocs.io) | HTML reports |
| [Allure](https://allurereport.org) | Rich test reports |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Environment config |
| GitHub Actions | CI/CD |

## Project Structure

```
├── pages/                  # Page Object Model
│   ├── base_page.py
│   ├── home_page.py
│   ├── catalog_page.py
│   ├── search_results_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   └── page_manager.py     # Single entry point to all pages
├── tests/
│   ├── test_home_page.py
│   ├── test_catalog.py
│   ├── test_search.py
│   ├── test_cart.py
│   ├── test_navigation.py
│   ├── test_ui.py
│   └── test_e2e.py         # Full end-to-end scenarios
├── reports/                # Auto-generated HTML reports
├── .github/workflows/
│   └── tests.yml           # CI/CD pipeline
├── conftest.py
├── pytest.ini
├── .env                    # Local environment variables (not committed)
└── Makefile
```

## Local Setup

**Requirements:** Python 3.12+

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install chromium
```

### Environment variables

Create a `.env` file in the project root (or copy from the example below):

```env
BASE_URL=https://www.21vek.by
BROWSER=chromium
HEADLESS=false
SLOW_MO=0
TIMEOUT=30000
```

## Running Tests

```bash
# All tests (HTML report generated automatically)
make test

# By category
make smoke
make regression
make e2e

# With Allure report (requires Allure CLI)
make allure

# Open the last HTML report in the browser
make report
```

Or run pytest directly:

```bash
pytest                            # all tests
pytest -m smoke                   # smoke only
pytest -m "smoke or regression"   # combined markers
pytest --headed                   # visible browser window
pytest --browser-name firefox     # specific browser
pytest --slow-mo 500              # slow motion (ms)
```

## Test Markers

| Marker | Description |
|---|---|
| `smoke` | Critical happy-path checks |
| `regression` | Full regression suite |
| `e2e` | End-to-end user journey scenarios |
| `catalog` | Catalog page tests |
| `search` | Search functionality |
| `cart` | Cart behaviour |
| `navigation` | Page navigation |
| `ui` | Visual / layout checks |

## CI/CD

The pipeline is triggered **manually** via **Actions → Run workflow** in GitHub.

### Inputs

| Input | Default | Description |
|---|---|---|
| `browser` | `chromium` | Browser to run tests in (`chromium`, `firefox`, `webkit`) |
| `markers` | _(empty)_ | pytest markers to filter tests; leave empty to run all |

### Secrets

Add the following secret in **Settings → Secrets and variables → Actions**:

| Secret | Value |
|---|---|
| `BASE_URL` | `https://www.21vek.by` |

### Pipeline steps

1. Checkout → install Python 3.12 → install dependencies → install Playwright
2. Run tests → collect Allure results
3. Generate Allure report with history
4. Deploy report to **GitHub Pages**
5. Upload artifacts (`allure-results`, `pytest-html-report`)
6. Write job summary with direct link to the report

The Allure report is available at `https://<owner>.github.io/<repo>/` after the first successful run.
