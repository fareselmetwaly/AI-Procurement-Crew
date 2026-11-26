import os
import sys
from pathlib import Path


def _find_project_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "pyproject.toml").exists() or (parent / "main.py").exists():
            return parent
    return start.parents[3]


CORE_DIR = Path(__file__).resolve().parent
ROOT_DIR = _find_project_root(CORE_DIR)
SRC_DIR = ROOT_DIR / "src"
CONFIG_DIR = SRC_DIR / "crew_project" / "crew" / "config"

os.environ["CREWAI_STORAGE_DIR"] = str(ROOT_DIR / ".crewai_storage")
TEMP_DIR = ROOT_DIR / ".temp"
TEMP_DIR.mkdir(exist_ok=True)
os.environ["TEMP"] = str(TEMP_DIR)
os.environ["TMP"] = str(TEMP_DIR)

os.chdir(ROOT_DIR)

for p in (str(SRC_DIR), str(ROOT_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

OUTPUT_DIR = ROOT_DIR / "data" / "ai-agent-output"
ENV_PATH = ROOT_DIR / ".env"

STEP_FILES = {
    "queries": "step1_suggested_search_queries.json",
    "search": "step2_search_results.json",
    "products": "step3_result_product_details.json",
    "report": "step_4_procurement_report.html",
    "metrics": "step5_metrics.json",
}

REPORT_PATH = OUTPUT_DIR / STEP_FILES["report"]
METRICS_PATH = OUTPUT_DIR / STEP_FILES["metrics"]
LATEST_CONFIG_PATH = OUTPUT_DIR / "latest_config.json"














"""
ROOT_DIR = Path(__file__)
print(ROOT_DIR)
ROOT_DIR = Path(__file__).resolve()
print(ROOT_DIR)
print("/"*50)
ROOT_DIR = Path(__file__).resolve().parent
print(ROOT_DIR)
print("/"*50)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
print(ROOT_DIR)
print("/"*50)

"""