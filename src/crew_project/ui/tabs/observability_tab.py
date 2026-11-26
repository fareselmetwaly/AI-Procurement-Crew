import json
import os
import gradio as gr

from crew_project.core.observability import (
    resolve_crewai_trace_url,
    resolve_opik_project_url,
)
from crew_project.core.paths import METRICS_PATH, ROOT_DIR
from crew_project.ui.renderers import render_metrics_dashboard


def load_latest_metrics_html() -> str:
    metrics = None
    if METRICS_PATH.exists():
        try:
            metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
        except Exception:
            metrics = None
    project = os.getenv("OPIK_PROJECT_NAME", "crew_project")
    return render_metrics_dashboard(
        metrics,
        opik_url=resolve_opik_project_url(project),
        opik_project=project,
        crewai_trace_url=resolve_crewai_trace_url(ROOT_DIR),
    )


def build_observability_tab():
    """Builds Tab 4 (Observability & Metrics)."""
    with gr.Tab("4. Observability & Metrics", id="observability") as obs_tab:
        with gr.Row():
            with gr.Column(scale=8):
                obs_header_md = gr.Markdown("### 📊 Observability, Token Metrics & CrewAI Tracing")
            with gr.Column(scale=2, min_width=180):
                refresh_btn = gr.Button("🔄 Refresh Metrics", size="sm")

        metrics_html = gr.HTML(load_latest_metrics_html())

    translatable = {
        "tab_obs": (obs_tab, "tab"),
        "obs_header_md": (obs_header_md, "md"),
        "refresh_metrics_btn": (refresh_btn, "btn"),
    }

    return {
        "id": "observability",
        "tab": obs_tab,
        "outputs": [metrics_html],
        "refresh_btn": refresh_btn,
        "translatable": translatable,
    }