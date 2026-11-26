import yaml
from crewai import Agent, Task

from crew_project.core.configurations import groq_llm
from crew_project.core.paths import CONFIG_DIR, OUTPUT_DIR, STEP_FILES
from crew_project.crew.tools.second_agent_tools import search_engine_tool
from crew_project.validation.second_agent_val import AllSearchResults

with open(CONFIG_DIR / "agents.yaml", "r", encoding="utf-8") as f:
    agents_config = yaml.safe_load(f)

with open(CONFIG_DIR / "tasks.yaml", "r", encoding="utf-8") as f:
    tasks_config = yaml.safe_load(f)

search_engine_agent = Agent(
    **agents_config["search_engine_agent"],
    tools=[search_engine_tool],
    llm=groq_llm,
    verbose=True,
)

search_engine_task = Task(
    **tasks_config["search_engine_task"],
    output_file=str(OUTPUT_DIR / STEP_FILES["search"]),
    output_json=AllSearchResults,
    agent=search_engine_agent,
)