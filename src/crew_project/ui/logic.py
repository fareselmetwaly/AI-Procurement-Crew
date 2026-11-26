import asyncio
import inspect
import json
import os
import threading
import time
from pathlib import Path

import gradio as gr
from pydantic import ValidationError

from crew_project.api.schemas import (
    ProcurementRequest,
    RuntimeSettingsRequest,
    format_validation_error,
)
from crew_project.core.observability import (
    OPIK_DASHBOARD_URL,
    resolve_crewai_trace_url,
    resolve_opik_project_url,
)
from crew_project.core.paths import (
    LATEST_CONFIG_PATH,
    METRICS_PATH,
    OUTPUT_DIR,
    REPORT_PATH,
    ROOT_DIR,
    STEP_FILES,
)
from crew_project.crew.run_crew import run_crew
from crew_project.crew.tools.tool_monitor import CrewStoppedException, request_stop
from crew_project.ui.config import STEP_TITLES
from crew_project.ui.renderers import (
    render_full_report_button,
    render_inputs_card,
    render_metrics_dashboard,
    render_products_grid,
    render_progress_report_link,
    render_queries_cards,
    render_report_iframe,
    render_search_results,
)


def build_config(
    company_name,
    about_company,
    product_name,
    purchase_strategy,
    budget,
    quantity,
    currency,
    extra_requirements,
    important_specs,
    websites_list,
    country_name,
    language,
    no_keywords,
    score_th,
    top_recommendations_no,
    exclude_israeli_supported,
    use_evaluator,
    max_iterations,
):
    """Validate inputs via Pydantic schema, save latest_config.json, and return config dict."""
    try:
        req = ProcurementRequest(
            company_name=company_name,
            about_company=about_company,
            product_name=product_name,
            purchase_strategy=purchase_strategy,
            budget=budget,
            quantity=quantity if quantity is not None else 1,
            currency=currency,
            extra_requirements=extra_requirements,
            important_specs=important_specs,
            websites_list=websites_list,
            country_name=country_name,
            language=language,
            no_keywords=no_keywords,
            score_th=score_th,
            top_recommendations_no=top_recommendations_no,
            exclude_israeli_supported=exclude_israeli_supported,
            use_evaluator=use_evaluator,
            max_iterations=max_iterations,
        )
    except ValidationError as e:
        raise gr.Error(format_validation_error(e))

    config = req.to_run_config()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(LATEST_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    return config


def _read_json(path: Path, started_at: float | None = None):
    """Return parsed JSON if valid (and optionally written after started_at)."""
    try:
        if not path.exists():
            return None
        if started_at is not None and path.stat().st_mtime < started_at:
            return None
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _worker(config, box, resume_mode=False):
    """Runs the crew in a side thread so the UI can keep updating."""
    try:
        os.chdir(ROOT_DIR)
        if inspect.iscoroutinefunction(run_crew):
            asyncio.run(run_crew(config, resume_mode=resume_mode))
        else:
            run_crew(config, resume_mode=resume_mode)
    except CrewStoppedException:
        box["stopped"] = True
    except Exception as e:
        box["error"] = f"{type(e).__name__}: {e}"
    finally:
        box["done"] = True


def _status(done_keys, error=None, stopped=False, warnings_count=0, finished=True):
    lines = []
    running_marked = False
    for key, title in STEP_TITLES:
        if key in done_keys:
            lines.append(f"✅ {title}")
        elif error or stopped:
            lines.append(f"⚪ {title}")
        elif not running_marked:
            lines.append(f"⏳ {title} ...")
            running_marked = True
        else:
            lines.append(f"⚪ {title}")

    text = "\n\n".join(lines)
    if stopped:
        text += "\n\n🛑 **Stopped by user.** Press **▶️ Resume Last Step** later to continue from the last completed step."
    elif error:
        text += f"\n\n❌ **Run failed:** {error}"
    elif len(done_keys) == len(STEP_TITLES) and not finished:
        # ملف التقرير ظهر لكن الـ crew لسه شغال (تنضيف الـ HTML / حلقة الـ Evaluator)
        text += "\n\n⏳ **Finalizing report** (cleanup / evaluator) ..."
    elif len(done_keys) == len(STEP_TITLES):
        if warnings_count > 0:
            text += f"\n\n⚠️ **Done with {warnings_count} warning(s)** — check **4. Observability & Metrics** for details."
        else:
            text += "\n\n🎉 **Done.**"
    return text


def request_stop_run():
    """Triggered immediately when the user clicks Stop Execution."""
    request_stop()
    gr.Warning("Stop signal sent — halting after current API call...")
    return gr.update(interactive=False, value="⏳ Stopping...")


def _execute_crew_generator(*args, resume_mode: bool = False):
    *values, current_state = args
    base_state = dict(current_state or {})

    if resume_mode and LATEST_CONFIG_PATH.exists():
        saved_cfg = _read_json(LATEST_CONFIG_PATH)
        config = saved_cfg if saved_cfg else build_config(*values)
    else:
        config = build_config(*values)

    started_at = time.time()
    box = {"done": False, "error": None, "stopped": False}
    threading.Thread(target=_worker, args=(config, box, resume_mode), daemon=True).start()

    data = {
        "queries": _read_json(OUTPUT_DIR / STEP_FILES["queries"]) if resume_mode else None,
        "search": _read_json(OUTPUT_DIR / STEP_FILES["search"]) if resume_mode else None,
        "products": _read_json(OUTPUT_DIR / STEP_FILES["products"]) if resume_mode else None,
        "metrics": None,
    }
    report_html = None

    def snapshot(first=False, is_running=True):
        done = {"config"} | {k for k in ("queries", "search", "products") if data[k] is not None}
        report_ready = report_html is not None
        if report_ready:
            done.add("report")

        w_count = int((data["metrics"] or {}).get("warnings_count") or 0)

        progress_values = [
            _status(done, box["error"], box["stopped"], w_count, finished=not is_running),
            render_inputs_card(config),
            render_queries_cards(data["queries"]),
            render_search_results(data["search"]),
            render_products_grid(data["products"]),
            render_progress_report_link(report_ready),
            str(REPORT_PATH) if report_ready else None,
        ]
        report_values = [
            render_full_report_button(report_ready),
            str(REPORT_PATH) if report_ready else None,
            render_report_iframe(report_html),
        ]

        project_name = os.getenv("OPIK_PROJECT_NAME", "crew_project")
        if first:
            # أول yield لازم يكون فوري: مفيش نداء شبكة لـ Opik هنا (ممكن يتأخر لو النت بطيء)
            opik_url, trace_url = OPIK_DASHBOARD_URL, None
        else:
            opik_url = resolve_opik_project_url(project_name)
            trace_url = resolve_crewai_trace_url(ROOT_DIR)
        obs_values = [
            render_metrics_dashboard(
                data["metrics"],
                opik_url=opik_url,
                opik_project=project_name,
                crewai_trace_url=trace_url,
            )
        ]
        new_state = {
            **base_state,
            "progress": progress_values,
            "report": report_values,
            "observability": obs_values,
        }
        run_btn_upd = (
            gr.update(interactive=False, value="⏳ Running...")
            if is_running
            else gr.update(interactive=True, value="Run")
        )
        resume_btn_upd = gr.update(interactive=not is_running)
        stop_btn_upd = gr.update(interactive=is_running, value="⏹️ Stop Execution")

        return (
            gr.Tabs(selected="progress") if first else gr.skip(),
            *progress_values,
            *report_values,
            *obs_values,
            run_btn_upd,
            resume_btn_upd,
            stop_btn_upd,
            new_state,
        )

    yield snapshot(first=True, is_running=True)
    last_sig = None
    while True:
        finished = box["done"]
        for key in ("queries", "search", "products", "metrics"):
            if data[key] is None:
                data[key] = _read_json(OUTPUT_DIR / STEP_FILES[key], started_at)

        if (
            report_html is None
            and REPORT_PATH.exists()
            and REPORT_PATH.stat().st_mtime >= started_at
        ):
            try:
                report_html = REPORT_PATH.read_text(encoding="utf-8")
            except OSError:
                pass

        if finished:
            if data["metrics"] is None:
                data["metrics"] = _read_json(METRICS_PATH, started_at)
            # التقرير بيتعدل بعد ما الـ Task يكتبه (تنضيف ```html وحلقة الـ Evaluator)،
            # فنقراه تاني من الملف النهائي عشان الـ preview يطابق اللي في /report
            try:
                if REPORT_PATH.exists() and REPORT_PATH.stat().st_mtime >= started_at:
                    report_html = REPORT_PATH.read_text(encoding="utf-8")
            except OSError:
                pass
            yield snapshot(is_running=False)
            break

        # ابعت تحديث للمتصفح بس لما يحصل تغيير فعلي (بدل ما نبعت كل الـ HTML والتقرير كل ثانية)
        sig = (
            tuple(k for k in ("queries", "search", "products", "metrics") if data[k] is not None),
            report_html is not None,
            box["error"],
            box["stopped"],
        )
        if sig != last_sig:
            last_sig = sig
            yield snapshot(is_running=True)
        time.sleep(1)


def on_run(*args):
    yield from _execute_crew_generator(*args, resume_mode=False)


def on_resume(*args):
    has_any_step = any(
        (OUTPUT_DIR / STEP_FILES[k]).exists() for k in ("queries", "search", "products")
    )
    if not has_any_step:
        raise gr.Error("No completed steps found to resume from. Press Run first.")
    yield from _execute_crew_generator(*args, resume_mode=True)

def save_runtime_settings(
    llm_model,
    llm_base_url,
    llm_temp,
    llm_max_tokens,
    groq_key,
    gemini_key,
    tavily_key,
    firecrawl_key,
    opik_key,
    opik_project,
):
    """Saves updated LLM/API settings to .env and reloads live clients immediately."""
    try:
        settings_req = RuntimeSettingsRequest(
            llm_model=llm_model,
            llm_base_url=llm_base_url,
            llm_temp=llm_temp if llm_temp is not None else 0.0,
            llm_max_tokens=llm_max_tokens or 4096,
            groq_key=groq_key,
            gemini_key=gemini_key,
            tavily_key=tavily_key,
            firecrawl_key=firecrawl_key,
            opik_key=opik_key,
            opik_project=opik_project,
        )
    except ValidationError as e:
        raise gr.Error(format_validation_error(e))

    from crew_project.core.configurations import reload_runtime_config
    from crew_project.ui.tabs.observability_tab import load_latest_metrics_html

    updates = settings_req.to_env_updates()
    reload_runtime_config(updates)
    gr.Info(f"Settings saved! Active model: {updates['LLM_MODEL_NAME']} | Opik: {updates['OPIK_PROJECT_NAME']}")
    return (
        f"✅ **Saved & applied!** Model: **`{updates['LLM_MODEL_NAME']}`** | Opik Project: **`{updates['OPIK_PROJECT_NAME']}`**.",
        load_latest_metrics_html(),
    )


def toggle_iterations(use_evaluator):
    return gr.update(visible=use_evaluator)


def make_tab_restorer(tab_id: str, num_outputs: int):
    """Generic handler that restores any tab's saved outputs from app_state."""
    def _restore(state):
        if not state or tab_id not in state:
            return [gr.skip()] * num_outputs
        return state[tab_id]
    return _restore