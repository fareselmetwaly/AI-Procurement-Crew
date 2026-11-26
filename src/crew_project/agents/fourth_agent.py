import yaml
from crewai import Agent, Task

from crew_project.core.configurations import groq_llm
from crew_project.core.paths import CONFIG_DIR, REPORT_PATH

with open(CONFIG_DIR / "agents.yaml", "r", encoding="utf-8") as f:
    agents_config = yaml.safe_load(f)

with open(CONFIG_DIR / "tasks.yaml", "r", encoding="utf-8") as f:
    tasks_config = yaml.safe_load(f)

procurement_report_author_agent = Agent(
    **agents_config["procurement_report_author_agent"],
    llm=groq_llm,
    verbose=True,
)

procurement_report_author_task = Task(
    **tasks_config["procurement_report_author_task"],
    output_file=str(REPORT_PATH),
    agent=procurement_report_author_agent,
)