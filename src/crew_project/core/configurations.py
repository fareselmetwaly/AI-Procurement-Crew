import json
import os
from dotenv import load_dotenv

from crewai import LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from firecrawl import Firecrawl
from opik import configure
from opik.integrations.crewai import track_crewai
from tavily import TavilyClient

from crew_project.core.paths import ENV_PATH, LATEST_CONFIG_PATH, OUTPUT_DIR

load_dotenv(dotenv_path=ENV_PATH, override=True)

# Track CrewAI runs with Opik
opik_api_key = os.getenv("OPIK_API_KEY", "")
opik_project_name = os.getenv("OPIK_PROJECT_NAME", "crew_project")
os.environ["OPIK_PROJECT_NAME"] = opik_project_name
if opik_api_key:
    os.environ["OPIK_API_KEY"] = opik_api_key
    try:
        configure(project_name=opik_project_name, api_key=opik_api_key)
        track_crewai(project_name=opik_project_name)
    except Exception:
        pass


def _build_llm(model_name: str, base_url: str, api_key: str, temperature: float, max_tokens: int) -> LLM:
    """Builds a CrewAI LLM supporting both custom OpenAI-compatible endpoints and native providers."""
    clean_model = model_name.strip()
    clean_url = (base_url or "").strip() or None
    known_prefixes = ("openai/", "groq/", "gemini/", "anthropic/", "ollama/", "huggingface/", "azure/", "deepseek/")

    if clean_url and not clean_model.startswith(known_prefixes):
        clean_model = f"openai/{clean_model}"

    kwargs = {
        "model": clean_model,
        "api_key": api_key,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if clean_url:
        kwargs["base_url"] = clean_url

    return LLM(**kwargs)


def _build_embedder(gemini_key: str) -> dict | None:
    """Returns Gemini embedder config only if GEMINI_API_KEY is provided."""
    key = (gemini_key or "").strip()
    if not key:
        return None
    return {
        "provider": "google-generativeai",
        "config": {
            "model_name": "gemini-embedding-001",
            "api_key": key,
        },
    }


# Model & Embedder config
groq_model_name = os.getenv("LLM_MODEL_NAME", "deepseek-v4-flash")
groq_api_key = os.getenv("GROQ_API_KEY", "")
groq_base_url = os.getenv("LLM_BASE_URL", "https://backend.sovereigneg.com/v1")
groq_temperature = float(os.getenv("LLM_TEMPERATURE", "0"))
groq_max_tokens = int(os.getenv("LLM_MAX_TOKENS", "4096"))
gemini_api_key = os.getenv("GEMINI_API_KEY", "")

groq_llm = _build_llm(groq_model_name, groq_base_url, groq_api_key, groq_temperature, groq_max_tokens)
embedding = _build_embedder(gemini_api_key)

# Search & Scraping clients
tavily_api_key = os.getenv("TAVILY_API_KEY", "")
tavily_client = TavilyClient(api_key=tavily_api_key) if tavily_api_key else None

firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY", "")
firecrawl_client = Firecrawl(api_key=firecrawl_api_key) if firecrawl_api_key else None

# Output folder (unified with core.paths)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
output_agent = str(OUTPUT_DIR)

if LATEST_CONFIG_PATH.exists():
    with open(LATEST_CONFIG_PATH, "r", encoding="utf-8") as file:
        config_inputs = json.load(file)
else:
    config_inputs = {}

company_name = config_inputs.get("company_name", "Rankyx")
about_company = config_inputs.get("about_company", "")
product_name = config_inputs.get("product_name", "")
purchase_strategy = config_inputs.get("purchase_strategy", "Value for price")
budget = config_inputs.get("budget", None)
quantity = config_inputs.get("quantity", 1)
currency = config_inputs.get("currency", "EGP")
extra_requirements = config_inputs.get("extra_requirements", "")
important_specs = config_inputs.get("important_specs", "")
websites_list = config_inputs.get("websites_list", [])
country_name = config_inputs.get("country_name", "Egypt")
language = config_inputs.get("language", "English")
no_keywords = config_inputs.get("no_keywords", 10)
score_th = config_inputs.get("score_th", 0.10)
top_recommendations_no = config_inputs.get("top_recommendations_no", 10)
exclude_israeli_supported = config_inputs.get("exclude_israeli_supported", True)
use_evaluator = config_inputs.get("use_evaluator", False)
max_iterations = config_inputs.get("max_iterations", 0)
current_date = config_inputs.get("current_date", "")
run_id = config_inputs.get("run_id", "")

company_context = StringKnowledgeSource(content=about_company or "General company context.")


def reload_runtime_config(updates: dict) -> None:
    """Updates .env, os.environ, and live LLM/Embedder/Tool/Opik clients without restarting."""
    global groq_model_name, groq_api_key, groq_base_url, groq_temperature, groq_max_tokens
    global groq_llm, gemini_api_key, embedding, tavily_api_key, tavily_client
    global firecrawl_api_key, firecrawl_client, opik_api_key, opik_project_name

    existing_lines = ENV_PATH.read_text(encoding="utf-8").splitlines() if ENV_PATH.exists() else []
    remaining = {k: str(v) for k, v in updates.items() if v is not None}
    new_lines = []

    for line in existing_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            new_lines.append(line)
            continue
        key = stripped.split("=", 1)[0].strip()
        if key in remaining:
            val = remaining.pop(key)
            if any(ch in val for ch in (" ", "#", '"', "'")):
                val = '"' + val.replace('"', '\\"') + '"'
            new_lines.append(f"{key}={val}")
        else:
            new_lines.append(line)

    for key, val in remaining.items():
        if any(ch in val for ch in (" ", "#", '"', "'")):
            val = '"' + val.replace('"', '\\"') + '"'
        new_lines.append(f"{key}={val}")

    ENV_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    load_dotenv(dotenv_path=ENV_PATH, override=True)

    groq_model_name = os.getenv("LLM_MODEL_NAME", groq_model_name)
    groq_api_key = os.getenv("GROQ_API_KEY", groq_api_key)
    groq_base_url = os.getenv("LLM_BASE_URL", "")
    groq_temperature = float(os.getenv("LLM_TEMPERATURE", str(groq_temperature)))
    groq_max_tokens = int(os.getenv("LLM_MAX_TOKENS", str(groq_max_tokens)))
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")

    groq_llm = _build_llm(groq_model_name, groq_base_url, groq_api_key, groq_temperature, groq_max_tokens)
    embedding = _build_embedder(gemini_api_key)

    tavily_api_key = os.getenv("TAVILY_API_KEY", "")
    tavily_client = TavilyClient(api_key=tavily_api_key) if tavily_api_key else None

    firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY", "")
    firecrawl_client = Firecrawl(api_key=firecrawl_api_key) if firecrawl_api_key else None

    opik_api_key = os.getenv("OPIK_API_KEY", "")
    opik_project_name = os.getenv("OPIK_PROJECT_NAME", "crew_project")
    os.environ["OPIK_PROJECT_NAME"] = opik_project_name
    if opik_api_key:
        os.environ["OPIK_API_KEY"] = opik_api_key
        try:
            configure(project_name=opik_project_name, api_key=opik_api_key, force=True)
            track_crewai(project_name=opik_project_name)
        except TypeError:
            configure(project_name=opik_project_name, api_key=opik_api_key)
            track_crewai(project_name=opik_project_name)
        except Exception:
            pass