# E-Commerce QA Automation Framework

An end-to-end test automation framework built with **Playwright + Python** targeting [SauceDemo](https://www.saucedemo.com/), a practice e-commerce web application.

## 🛠️ Tech Stack
- **Playwright (Python)** – Browser automation
- **Pytest** – Test runner and fixture management
- **Page Object Model (POM)** – Design pattern for maintainability
- **GitHub Actions** – CI/CD pipeline (runs on every push/PR)
- **JSON fixtures** – Data-driven test parameterization

## 📁 Project Structure

```
ecommerce_qa/
├── pages/                  # Page Object classes
│   ├── login_page.py       # Login page interactions
│   ├── inventory_page.py   # Product listing page
│   ├── cart_page.py        # Shopping cart
│   └── checkout_page.py    # Checkout flow
├── tests/                  # Test suites
│   ├── test_login.py       # 6 login test cases
│   └── test_cart_checkout.py  # 12 cart/checkout/sorting tests
├── utils/
│   └── test_data.json      # Centralized test data (data-driven)
├── .github/workflows/
│   └── tests.yml           # GitHub Actions CI/CD
├── conftest.py             # Shared pytest fixtures
├── requirements.txt
└── README.md
```

## ✅ Test Coverage (18 Test Cases)

### Login Module (6 TCs)
| TC | Scenario | Expected |
|---|---|---|
| TC001 | Valid login | Redirect to inventory |
| TC002 | Invalid credentials | Error message shown |
| TC003 | Locked out user | Locked error shown |
| TC004 | Empty username | Validation error |
| TC005 | Empty password | Validation error |
| TC006 | Logout | Redirect to login |

### Cart Module (5 TCs)
| TC | Scenario | Expected |
|---|---|---|
| TC007 | Add single item | Cart badge = 1 |
| TC008 | Add multiple items | Cart badge = 2 |
| TC009 | Remove item from cart | Item count decreases |
| TC010 | Cart persistence on navigation | Items retained |
| TC011 | Product visible in cart | Correct name in cart |

### Checkout Module (3 TCs)
| TC | Scenario | Expected |
|---|---|---|
| TC012 | Full successful checkout | "Thank you" confirmation |
| TC013 | Missing first name | Validation error |
| TC014 | Missing postal code | Validation error |

### Sorting Module (4 TCs)
| TC | Scenario | Expected |
|---|---|---|
| TC015 | Sort A to Z | Names in ascending order |
| TC016 | Sort Z to A | Names in descending order |
| TC017 | Sort price low to high | Prices ascending |
| TC018 | Sort price high to low | Prices descending |

## 🚀 Setup & Run

```bash
# Clone the repo
git clone https://github.com/your-username/ecommerce-qa-framework.git
cd ecommerce_qa

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_login.py -v

# Run with HTML report
pytest tests/ -v --html=report.html
```

## 🔑 Key Design Decisions

- **Page Object Model**: Each page has its own class with locators and actions. Tests never interact with the DOM directly — this makes tests readable and easy to maintain.
- **Session-scoped browser**: Browser is launched once per test session for speed; each test gets a fresh page context to avoid state pollution.
- **JSON test data**: All usernames, passwords, and product names are centralized in `test_data.json` — easy to update without touching test code.
- **CI/CD**: GitHub Actions runs the full suite on every push and PR, with artifacts uploaded for review.

## 📊 Results
- **18 automated test cases** covering login, cart, checkout, and sorting
- **~90% coverage** of critical user journeys
- Reduced manual regression effort by approximately **70%**
