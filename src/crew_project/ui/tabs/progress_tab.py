import gradio as gr
from crew_project.ui.renderers import render_empty_box


def build_progress_tab():
    """Builds Tab 2 (Progress) with clean visual cards and immediate Stop control."""
    with gr.Tab("2. Progress", id="progress") as progress_tab:
        with gr.Row():
            with gr.Column(scale=8):
                status_md = gr.Markdown("Press **Run** in the Inputs tab.")
            with gr.Column(scale=2, min_width=180):
                stop_btn = gr.Button("⏹️ Stop Execution", variant="stop", interactive=False)

        with gr.Accordion("0. Inputs (Request Summary)", open=True) as acc_p0:
            config_view = gr.HTML(render_empty_box("Waiting for run..."))
        with gr.Accordion("1. Search Queries Agent", open=True) as acc_p1:
            queries_view = gr.HTML(render_empty_box("Waiting for Search Queries Agent..."))
        with gr.Accordion("2. Search Engine Agent", open=False) as acc_p2:
            search_view = gr.HTML(render_empty_box("Waiting for Search Engine Agent..."))
        with gr.Accordion("3. Web Scraping Agent", open=True) as acc_p3:
            products_view = gr.HTML(render_empty_box("Waiting for Web Scraping Agent..."))
        with gr.Accordion("4. Report Author Agent", open=True) as acc_p4:
            report_link = gr.HTML("<i>Report not ready yet...</i>")
            report_file = gr.File(label="Download report (HTML)")

    translatable = {
        "tab_progress": (progress_tab, "tab"),
        "stop_btn": (stop_btn, "btn"),
        "acc_p0": (acc_p0, "label"),
        "acc_p1": (acc_p1, "label"),
        "acc_p2": (acc_p2, "label"),
        "acc_p3": (acc_p3, "label"),
        "acc_p4": (acc_p4, "label"),
        "report_file": (report_file, "label"),
    }

    return {
        "id": "progress",
        "tab": progress_tab,
        "stop_btn": stop_btn,
        "outputs": [
            status_md,
            config_view,
            queries_view,
            search_view,
            products_view,
            report_link,
            report_file,
        ],
        "translatable": translatable,
    }