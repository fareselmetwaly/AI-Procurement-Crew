import yaml
from crewai import Agent, Task

from crew_project.core.configurations import groq_llm
from crew_project.core.paths import CONFIG_DIR, OUTPUT_DIR, STEP_FILES
from crew_project.validation.first_agent_val import SearchQueriesJSON

with open(CONFIG_DIR / "agents.yaml", "r", encoding="utf-8") as f:
    agents_config = yaml.safe_load(f)

with open(CONFIG_DIR / "tasks.yaml", "r", encoding="utf-8") as f:
    tasks_config = yaml.safe_load(f)

search_queries_agent = Agent(
    **agents_config["search_queries_agent"],
    llm=groq_llm,
    verbose=True,
)

search_queries_task = Task(
    **tasks_config["search_queries_task"],
    output_json=SearchQueriesJSON,
    output_file=str(OUTPUT_DIR / STEP_FILES["queries"]),
    agent=search_queries_agent,
)