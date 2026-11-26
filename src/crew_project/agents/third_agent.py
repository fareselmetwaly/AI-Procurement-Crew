import yaml
from crewai import Agent, Task

from crew_project.core.configurations import groq_llm
from crew_project.core.paths import CONFIG_DIR, OUTPUT_DIR, STEP_FILES
from crew_project.crew.tools.third_agent_tools import web_scraping_tool
from crew_project.validation.third_agent_val import ExtractedProducts

with open(CONFIG_DIR / "agents.yaml", "r", encoding="utf-8") as f:
    agents_config = yaml.safe_load(f)

with open(CONFIG_DIR / "tasks.yaml", "r", encoding="utf-8") as f:
    tasks_config = yaml.safe_load(f)

web_scraping_agent = Agent(
    **agents_config["web_scraping_agent"],
    tools=[web_scraping_tool],
    llm=groq_llm,
    verbose=True,
)

web_scraping_task = Task(
    **tasks_config["web_scraping_task"],
    output_file=str(OUTPUT_DIR / STEP_FILES["products"]),
    output_json=ExtractedProducts,
    agent=web_scraping_agent,
)