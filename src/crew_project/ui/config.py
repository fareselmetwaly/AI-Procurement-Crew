from crew_project.core.observability import OPIK_DASHBOARD_URL
from crew_project.core.paths import (
    ENV_PATH,
    LATEST_CONFIG_PATH,
    METRICS_PATH,
    OUTPUT_DIR,
    REPORT_PATH,
    ROOT_DIR,
    STEP_FILES,
)

STEP_TITLES = [
    ("config", "0. Inputs"),
    ("queries", "1. Search Queries Agent"),
    ("search", "2. Search Engine Agent"),
    ("products", "3. Web Scraping Agent"),
    ("report", "4. Report Author Agent"),
]

EXAMPLE = {
    "company_name": "Rankyx",
    "about_company": (
        "Rankyx is a company that provides AI solutions to help websites "
        "refine their search and recommendation systems."
    ),
    "product_name": "coffee machine for the office",
    "purchase_strategy": "Value for price",
    "budget": None,
    "quantity": 1,
    "currency": "EGP",
    "extra_requirements": "",
    "important_specs": "",
    "websites_list": "www.amazon.eg\nwww.jumia.com.eg\nwww.noon.com/egypt-en",
    "country_name": "Egypt",
    "language": "English",
    "no_keywords": 10,
    "score_th": 0.10,
    "top_recommendations_no": 10,
    "exclude_israeli_supported": True,
    "use_evaluator": False,
    "max_iterations": 2,
}

EXAMPLE_KEYS = [
    "company_name", "about_company", "product_name", "purchase_strategy",
    "budget", "quantity", "currency", "extra_requirements", "important_specs",
    "websites_list", "country_name", "language", "no_keywords",
    "score_th", "top_recommendations_no", "exclude_israeli_supported",
    "use_evaluator", "max_iterations",
]

STRATEGIES = ["Value for price", "Lowest price", "Highest quality"]
CURRENCIES = ["EGP", "SAR", "AED", "USD", "EUR"]
LANGUAGES = ["English", "Arabic"]

MODEL_CHOICES = [
    "deepseek-v4-flash",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
    "qwen-qwq-32b",
    "gemini/gemini-2.5-flash",
    "gpt-4o-mini",
]