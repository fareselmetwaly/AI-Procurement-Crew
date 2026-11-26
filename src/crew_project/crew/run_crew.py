from copy import copy
from datetime import datetime
import json
import re
import time
from pathlib import Path

from crewai import Crew, Process
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

from crew_project.core.paths import METRICS_PATH, OUTPUT_DIR, REPORT_PATH, STEP_FILES


def _clean_html_report(report_path: Path) -> None:
    """Removes any conversational intro/outro or ```html markdown fences from the report."""
    if not report_path.exists():
        return

    raw = report_path.read_text(encoding="utf-8")

    cleaned = re.sub(r"^```(?:html)?\s*", "", raw.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned.strip())

    doc_match = re.search(r"(<!DOCTYPE html>|<html\b)", cleaned, flags=re.IGNORECASE)
    if doc_match:
        cleaned = cleaned[doc_match.start():]

    end_match = re.search(r"</html>", cleaned, flags=re.IGNORECASE)
    if end_match:
        cleaned = cleaned[: end_match.end()]

    report_path.write_text(cleaned.strip(), encoding="utf-8")


def _prepare_inputs(config: dict) -> dict:
    """Prepares safe, formatted prompt variables from UI config so no None/list breaks interpolation."""
    inputs = dict(config)

    raw_date = config.get("current_date") or datetime.now().strftime("%Y-%m-%d")
    try:
        dt = datetime.strptime(raw_date, "%Y-%m-%d")
        full_date = dt.strftime("%A, %B %d, %Y")
    except ValueError:
        full_date = raw_date

    websites = config.get("websites_list") or []
    websites_text = ", ".join(websites) if isinstance(websites, list) else str(websites)

    budget = config.get("budget")
    currency = config.get("currency", "EGP")
    budget_text = f"{budget} {currency}" if budget else f"Flexible (no strict cap, all prices in {currency})"

    important_specs = (config.get("important_specs") or "").strip()
    important_specs_text = important_specs if important_specs else "Standard best-in-class specifications"

    extra_req = (config.get("extra_requirements") or "").strip()
    extra_requirements_text = extra_req if extra_req else "None"

    exclude_il = bool(config.get("exclude_israeli_supported", True))
    israeli_filter_rule = (
        "STRICTLY EXCLUDE any product, brand, or parent company that supports Israel."
        if exclude_il
        else "No brand origin restriction."
    )

    inputs.update({
        "current_date": raw_date,
        "full_date": full_date,
        "websites_text": websites_text,
        "budget_text": budget_text,
        "important_specs_text": important_specs_text,
        "extra_requirements_text": extra_requirements_text,
        "israeli_filter_rule": israeli_filter_rule,
    })

    for k, v in list(inputs.items()):
        if v is None:
            inputs[k] = "Not specified"

    return inputs


def _get_llm_usage_snapshot(llm) -> dict:
    """Safely reads cumulative token usage from the CrewAI LLM instance."""
    try:
        summary = llm.get_token_usage_summary()
        if hasattr(summary, "model_dump"):
            return summary.model_dump()
        if isinstance(summary, dict):
            return dict(summary)
    except Exception:
        pass
    return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "successful_requests": 0}


def _load_valid_checkpoint(path: Path) -> str | None:
    """Reads a step JSON file if it exists and is valid non-empty JSON."""
    if not path.exists():
        return None
    try:
        raw = path.read_text(encoding="utf-8").strip()
        data = json.loads(raw)
        if data:
            return json.dumps(data, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return None


def run_crew(config: dict, resume_mode: bool = False):
    from crew_project.core.configurations import embedding, groq_llm
    from crew_project.agents.first_agent import search_queries_agent, search_queries_task
    from crew_project.agents.second_agent import search_engine_agent, search_engine_task
    from crew_project.agents.third_agent import web_scraping_agent, web_scraping_task
    from crew_project.agents.fourth_agent import procurement_report_author_agent, procurement_report_author_task
    from crew_project.crew.tools.tool_monitor import check_stop, clear_stop, get_tool_events, reset_tool_events

    for _ag in (search_queries_agent, search_engine_agent, web_scraping_agent, procurement_report_author_agent):
        _ag.llm = groq_llm

    clear_stop()
    if not resume_mode:
        reset_tool_events()

    about_text = (config.get("about_company") or "").strip() or "General procurement request."
    crew_inputs = _prepare_inputs(config)

    steps = [
        ("queries", 1, search_queries_agent, search_queries_task, OUTPUT_DIR / STEP_FILES["queries"]),
        ("search", 2, search_engine_agent, search_engine_task, OUTPUT_DIR / STEP_FILES["search"]),
        ("products", 3, web_scraping_agent, web_scraping_task, OUTPUT_DIR / STEP_FILES["products"]),
        ("report", 4, procurement_report_author_agent, procurement_report_author_task, REPORT_PATH),
    ]

    active_agents = []
    active_tasks = []
    step_numbers = []
    checkpoint_context_blocks = []

    if resume_mode:
        for key, step_no, ag, tsk, fpath in steps:
            if key != "report":
                ckpt = _load_valid_checkpoint(fpath)
                if ckpt and not active_tasks:
                    checkpoint_context_blocks.append(f"--- Completed Step {step_no} ({key}) Data ---\n{ckpt}")
                    continue
            tsk_copy = copy(tsk)
            if not active_tasks and checkpoint_context_blocks:
                injected = "\n\n".join(checkpoint_context_blocks)
                tsk_copy.description = (
                    f"{tsk.description}\n\n"
                    f"Use these verified results already completed in previous steps:\n{injected}"
                )
            active_agents.append(ag)
            active_tasks.append(tsk_copy)
            step_numbers.append(step_no)
    else:
        for _, step_no, ag, tsk, _ in steps:
            active_agents.append(ag)
            active_tasks.append(copy(tsk))
            step_numbers.append(step_no)

    t0 = time.perf_counter()
    tracker = {
        "last_time": t0,
        "last_usage": _get_llm_usage_snapshot(groq_llm),
        "agents": [],
    }

    def on_task_complete(task_output):
        check_stop()
        now = time.perf_counter()
        cur_usage = _get_llm_usage_snapshot(groq_llm)
        prev_usage = tracker["last_usage"]

        idx = len(tracker["agents"])
        step_num = step_numbers[idx] if idx < len(step_numbers) else idx + 1
        tracker["agents"].append({
            "step": step_num,
            "agent": getattr(task_output, "agent", f"Agent {step_num}"),
            "duration_sec": round(now - tracker["last_time"], 2),
            "prompt_tokens": max(0, cur_usage.get("prompt_tokens", 0) - prev_usage.get("prompt_tokens", 0)),
            "completion_tokens": max(0, cur_usage.get("completion_tokens", 0) - prev_usage.get("completion_tokens", 0)),
            "total_tokens": max(0, cur_usage.get("total_tokens", 0) - prev_usage.get("total_tokens", 0)),
            "llm_calls": max(0, cur_usage.get("successful_requests", 0) - prev_usage.get("successful_requests", 0)),
        })

        tracker["last_time"] = now
        tracker["last_usage"] = cur_usage

    crew_kwargs = {
        "agents": active_agents,
        "tasks": active_tasks,
        "process": Process.sequential,
        "task_callback": on_task_complete,
        "step_callback": lambda _: check_stop(),
        "tracing": True,
    }
    if embedding:
        crew_kwargs["knowledge_sources"] = [StringKnowledgeSource(content=about_text)]
        crew_kwargs["embedder"] = embedding
    elif active_tasks:
        active_tasks[0].description = f"Company Context: {about_text}\n\n{active_tasks[0].description}"

    crew = Crew(**crew_kwargs)
    result = crew.kickoff(inputs=crew_inputs)

    _clean_html_report(REPORT_PATH)

    if config.get("use_evaluator") and int(config.get("max_iterations", 0)) > 0:
        check_stop()
        evaluator_file = Path(__file__).resolve().parent.parent / "agents" / "evaluator_agent.py"
        if evaluator_file.exists():
            from crew_project.agents.evaluator_agent import run_evaluator_loop
            run_evaluator_loop(config=crew_inputs, report_path=REPORT_PATH, max_iterations=int(config["max_iterations"]))
            _clean_html_report(REPORT_PATH)

    total_seconds = round(time.perf_counter() - t0, 2)
    final_usage = _get_llm_usage_snapshot(groq_llm)
    if not final_usage.get("total_tokens"):
        tu = getattr(result, "token_usage", None)
        if tu:
            final_usage = tu.model_dump() if hasattr(tu, "model_dump") else dict(tu)

    tool_events = get_tool_events()
    warnings = [ev for ev in tool_events if ev["status"] in ("warning", "error")]

    metrics_payload = {
        "run_id": config.get("run_id", ""),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "status": "completed_with_warnings" if warnings else "success",
        "warnings_count": len(warnings),
        "warnings": warnings,
        "tool_events": tool_events,
        "totals": {
            "total_duration_sec": total_seconds,
            "prompt_tokens": final_usage.get("prompt_tokens", 0),
            "completion_tokens": final_usage.get("completion_tokens", 0),
            "total_tokens": final_usage.get("total_tokens", 0),
            "llm_calls": final_usage.get("successful_requests", 0),
        },
        "agents": tracker["agents"],
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(
        json.dumps(metrics_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return result