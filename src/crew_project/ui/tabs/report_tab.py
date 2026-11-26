import gradio as gr
from crew_project.core.paths import REPORT_PATH
from crew_project.ui.renderers import render_full_report_button, render_report_iframe


def build_report_tab():
    """Builds Tab 3 (Final Report) with live embedded preview and download."""
    initial_html = REPORT_PATH.read_text(encoding="utf-8") if REPORT_PATH.exists() else None
    initial_link = render_full_report_button(
        bool(initial_html),
        empty_msg="Run the crew to generate the report.",
    )

    with gr.Tab("3. Final Report", id="report") as report_tab:
        report_header_md = gr.Markdown(
            "### 📄 Executive Procurement Report\n"
            "Preview the generated report below, open it in a full browser tab, or download it."
        )
        with gr.Row():
            report_top_link = gr.HTML(initial_link)
            report_download = gr.File(
                label="Download Report (HTML)",
                value=str(REPORT_PATH) if initial_html else None,
            )
        report_iframe = gr.HTML(render_report_iframe(initial_html))

    translatable = {
        "tab_report": (report_tab, "tab"),
        "report_header_md": (report_header_md, "md"),
        "report_download": (report_download, "label"),
    }

    return {
        "id": "report",
        "tab": report_tab,
        "outputs": [report_top_link, report_download, report_iframe],
        "translatable": translatable,
    }