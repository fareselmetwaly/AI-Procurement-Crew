import gradio as gr
from crew_project.ui.config import CURRENCIES, EXAMPLE, LANGUAGES, STRATEGIES
from crew_project.ui.json_io import build_template_json_file

def build_inputs_tab():
    """Builds Tab 1 (Inputs) and returns a standard tab contract."""
    with gr.Tab("1. Inputs", id="inputs") as inputs_tab:
        basics_md = gr.Markdown("### Basics")
        with gr.Row():
            company_name = gr.Textbox(label="Company name", value=EXAMPLE["company_name"])
            product_name = gr.Textbox(
                label="Product *",
                value=EXAMPLE["product_name"],
                placeholder="e.g. coffee machine for the office",
            )
        websites_list = gr.Textbox(
            label="Websites (one per line) *",
            value=EXAMPLE["websites_list"],
            lines=3,
        )
        with gr.Row():
            country_name = gr.Textbox(label="Country", value=EXAMPLE["country_name"])
            purchase_strategy = gr.Dropdown(
                STRATEGIES, label="Purchase strategy", value=EXAMPLE["purchase_strategy"]
            )

        with gr.Accordion("Company details", open=False) as acc_company:
            about_company = gr.Textbox(
                label="About the company", value=EXAMPLE["about_company"], lines=3
            )

        with gr.Accordion("Request details", open=False) as acc_request:
            with gr.Row():
                budget = gr.Number(label="Budget (optional)", value=EXAMPLE["budget"])
                quantity = gr.Number(label="Quantity", value=EXAMPLE["quantity"], precision=0)
                currency = gr.Dropdown(CURRENCIES, label="Currency", value=EXAMPLE["currency"])
            extra_requirements = gr.Textbox(
                label="Extra requirements (optional)",
                placeholder="warranty, delivery, must-have features...",
                lines=2,
            )
            important_specs = gr.Textbox(
                label="Important specs (optional)",
                placeholder="capacity, power, warranty",
            )

        with gr.Accordion("Search & filtering", open=False) as acc_search:
            with gr.Row():
                language = gr.Dropdown(
                    LANGUAGES, label="Search keywords language", value=EXAMPLE["language"]
                )
                no_keywords = gr.Slider(
                    3, 15, value=EXAMPLE["no_keywords"], step=1, label="Number of search queries"
                )
            with gr.Row():
                score_th = gr.Slider(
                    0.0, 1.0, value=EXAMPLE["score_th"], step=0.05, label="Min search score (Tavily)"
                )
                top_recommendations_no = gr.Slider(
                    1, 20, value=EXAMPLE["top_recommendations_no"], step=1, label="Number of products to extract"
                )
            exclude_israeli_supported = gr.Checkbox(
                label="Exclude products/companies that support Israel (The Wall filter)",
                value=EXAMPLE["exclude_israeli_supported"],
            )

        with gr.Accordion("Evaluator (optional)", open=False) as acc_evaluator:
            use_evaluator = gr.Checkbox(
                label="Enable Evaluator-Optimizer loop", value=EXAMPLE["use_evaluator"]
            )
            max_iterations = gr.Slider(
                1, 3, value=EXAMPLE["max_iterations"], step=1, label="Max iterations", visible=False
            )

        with gr.Accordion("📋 JSON Import/Export Guide (Required vs Optional)", open=False):
            gr.Markdown(
                "- **Key order does not matter** — each value maps automatically by its key name.\n"
                "- **Required keys (4):** `company_name`, `product_name`, `websites_list`, `country_name`.\n"
                "- **Optional keys (14):** `about_company`, `purchase_strategy`, `budget`, `quantity`, `currency`, "
                "`extra_requirements`, `important_specs`, `language`, `no_keywords`, `score_th`, "
                "`top_recommendations_no`, `exclude_israeli_supported`, `use_evaluator`, `max_iterations` "
                "*(any omitted key uses its default value)*."
            )

        with gr.Row():
            import_btn = gr.UploadButton("📥 Import JSON", file_types=[".json"], size="sm")
            export_btn = gr.DownloadButton(
                "📤 Export / Template JSON", value=build_template_json_file(), size="sm"
            )

        with gr.Row():
            example_btn = gr.Button("Load example")
            resume_btn = gr.Button("▶️ Resume Last Step", variant="secondary")
            run_btn = gr.Button("Run", variant="primary")

    all_inputs = [
        company_name, about_company, product_name, purchase_strategy,
        budget, quantity, currency, extra_requirements, important_specs,
        websites_list, country_name, language, no_keywords,
        score_th, top_recommendations_no, exclude_israeli_supported,
        use_evaluator, max_iterations,
    ]

    translatable = {
        "tab_inputs": (inputs_tab, "tab"),
        "basics_md": (basics_md, "md"),
        "company_name": (company_name, "label"),
        "product_name": (product_name, "label"),
        "websites_list": (websites_list, "label"),
        "country_name": (country_name, "label"),
        "purchase_strategy": (purchase_strategy, "label"),
        "acc_company": (acc_company, "label"),
        "about_company": (about_company, "label"),
        "acc_request": (acc_request, "label"),
        "budget": (budget, "label"),
        "quantity": (quantity, "label"),
        "currency": (currency, "label"),
        "extra_requirements": (extra_requirements, "label"),
        "important_specs": (important_specs, "label"),
        "acc_search": (acc_search, "label"),
        "language": (language, "label"),
        "no_keywords": (no_keywords, "label"),
        "score_th": (score_th, "label"),
        "top_recommendations_no": (top_recommendations_no, "label"),
        "exclude_israeli_supported": (exclude_israeli_supported, "label"),
        "acc_evaluator": (acc_evaluator, "label"),
        "use_evaluator": (use_evaluator, "label"),
        "max_iterations": (max_iterations, "label"),
        "example_btn": (example_btn, "btn"),
        "resume_btn": (resume_btn, "btn"),
        "run_btn": (run_btn, "btn"),
    }

    return {
        "id": "inputs",
        "tab": inputs_tab,
        "outputs": None,
        "all_inputs": all_inputs,
        "use_evaluator": use_evaluator,
        "max_iterations": max_iterations,
        "import_btn": import_btn,
        "export_btn": export_btn,
        "example_btn": example_btn,
        "resume_btn": resume_btn,
        "run_btn": run_btn,
        "translatable": translatable,
    }