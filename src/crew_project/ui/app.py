import crew_project.ui.config as config  # يتهيأ الأول عشان يظبط sys.path والمسارات

import gradio as gr

from crew_project.ui.config import EXAMPLE, EXAMPLE_KEYS
from crew_project.ui.json_io import export_inputs_json, import_inputs_json
from crew_project.ui.logic import (
    make_tab_restorer,
    on_resume,
    on_run,
    request_stop_run,
    save_runtime_settings,
    toggle_iterations,
)

from crew_project.ui.styles import (
    EYE_COMFORT_CSS,
    EYE_COMFORT_THEME,
    LOAD_THEME_JS,
    TOGGLE_THEME_JS,
)
from crew_project.ui.tabs.inputs_tab import build_inputs_tab
from crew_project.ui.tabs.observability_tab import build_observability_tab, load_latest_metrics_html
from crew_project.ui.tabs.progress_tab import build_progress_tab
from crew_project.ui.tabs.report_tab import build_report_tab
from crew_project.ui.tabs.settings_tab import build_settings_tab
from crew_project.ui.translations import TEXTS


with gr.Blocks(title="Procurement Crew", theme=EYE_COMFORT_THEME, css=EYE_COMFORT_CSS) as demo:
    with gr.Row():
        with gr.Column(scale=7):
            header_md = gr.Markdown(TEXTS["en"]["header_md"])
        with gr.Column(scale=3, min_width=260):
            with gr.Row():
                lang_btn = gr.Button(TEXTS["en"]["lang_btn"], size="sm")
                theme_btn = gr.Button("🌙 Dark Mode", size="sm")

    app_state = gr.State({})
    ui_lang_state = gr.State("en")

    with gr.Tabs() as tabs:
        inputs_ui = build_inputs_tab()
        progress_ui = build_progress_tab()
        report_ui = build_report_tab()
        obs_ui = build_observability_tab()
        settings_ui = build_settings_tab()

    registered_tabs = [
        inputs_ui,
        progress_ui,
        report_ui,
        obs_ui,
        settings_ui,
    ]

    for tab_info in registered_tabs:
        outputs = tab_info.get("outputs")
        if outputs and "tab" in tab_info:
            tab_info["tab"].select(
                fn=make_tab_restorer(tab_info["id"], len(outputs)),
                inputs=app_state,
                outputs=outputs,
            )

    all_translatable = {}
    for t_ui in registered_tabs:
        all_translatable.update(t_ui.get("translatable", {}))

    trans_keys = list(all_translatable.keys())

    # فحص بدري: أي key في translatable ملوش ترجمة في اللغتين يطلع تحذير في الـ terminal بدل ما يبوظ الواجهة بصمت
    _missing = [(lang, k) for lang in TEXTS for k in trans_keys if k not in TEXTS[lang]]
    if _missing:
        print(f"[ui.translations] WARNING: missing translations: {_missing}")
    trans_components = [all_translatable[k][0] for k in trans_keys]
    trans_kinds = [all_translatable[k][1] for k in trans_keys]

    def toggle_ui_language(cur_lang: str):
        new_lang = "ar" if cur_lang == "en" else "en"
        t = TEXTS[new_lang]
        updates = []
        for key, kind in zip(trans_keys, trans_kinds):
            txt = t.get(key)
            if txt is None:  # مفيش ترجمة للـ key ده -> سيبه زي ما هو بدل ما نكتب اسم الـ key في الواجهة
                updates.append(gr.skip())
            elif kind in ("md", "btn"):
                updates.append(gr.update(value=txt))
            else:
                updates.append(gr.update(label=txt))
        return (
            new_lang,
            gr.update(value=t["lang_btn"]),
            gr.update(value=t["header_md"]),
            *updates,
        )

    lang_btn.click(
        fn=toggle_ui_language,
        inputs=[ui_lang_state],
        outputs=[ui_lang_state, lang_btn, header_md, *trans_components],
    )

    theme_btn.click(fn=None, inputs=None, outputs=[theme_btn], js=TOGGLE_THEME_JS)
    demo.load(fn=None, inputs=None, outputs=[theme_btn], js=LOAD_THEME_JS)

    # Wiring
    inputs_ui["use_evaluator"].change(
        toggle_iterations,
        inputs_ui["use_evaluator"],
        inputs_ui["max_iterations"],
    )

    inputs_ui["import_btn"].upload(
        fn=import_inputs_json,
        inputs=[inputs_ui["import_btn"]],
        outputs=inputs_ui["all_inputs"],
    )

    inputs_ui["export_btn"].click(
        fn=export_inputs_json,
        inputs=inputs_ui["all_inputs"],
        outputs=[inputs_ui["export_btn"]],
    )

    inputs_ui["example_btn"].click(
        lambda: [EXAMPLE[k] for k in EXAMPLE_KEYS],
        None,
        inputs_ui["all_inputs"],
    )

    run_outputs = [
        tabs,
        *progress_ui["outputs"],
        *report_ui["outputs"],
        *obs_ui["outputs"],
        inputs_ui["run_btn"],
        inputs_ui["resume_btn"],
        progress_ui["stop_btn"],
        app_state,
    ]

    inputs_ui["run_btn"].click(
        on_run,
        [*inputs_ui["all_inputs"], app_state],
        run_outputs,
    )

    inputs_ui["resume_btn"].click(
        on_resume,
        [*inputs_ui["all_inputs"], app_state],
        run_outputs,
    )

    progress_ui["stop_btn"].click(
        fn=request_stop_run,
        inputs=None,
        outputs=[progress_ui["stop_btn"]],
    )

    obs_ui["refresh_btn"].click(
        fn=load_latest_metrics_html,
        inputs=None,
        outputs=obs_ui["outputs"],
    )

    settings_ui["save_btn"].click(
        fn=save_runtime_settings,
        inputs=settings_ui["all_settings"],
        outputs=[settings_ui["save_status"], *obs_ui["outputs"]],
    )