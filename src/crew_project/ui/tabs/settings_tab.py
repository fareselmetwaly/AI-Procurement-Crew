import os
from dotenv import load_dotenv
import gradio as gr
from crew_project.ui.config import ENV_PATH, MODEL_CHOICES


def build_settings_tab():
    """Builds Tab 5 (Configuration) for switching LLM providers, models, and API keys."""
    load_dotenv(dotenv_path=ENV_PATH, override=True)

    cur_model = os.getenv("LLM_MODEL_NAME", "deepseek-v4-flash")
    cur_base_url = os.getenv("LLM_BASE_URL", "https://backend.sovereigneg.com/v1")
    cur_temp = float(os.getenv("LLM_TEMPERATURE", "0"))
    cur_max_tokens = int(os.getenv("LLM_MAX_TOKENS", "4096"))
    cur_groq_key = os.getenv("GROQ_API_KEY", "")
    cur_gemini_key = os.getenv("GEMINI_API_KEY", "")
    cur_tavily_key = os.getenv("TAVILY_API_KEY", "")
    cur_firecrawl_key = os.getenv("FIRECRAWL_API_KEY", "")
    cur_opik_key = os.getenv("OPIK_API_KEY", "")
    cur_opik_project = os.getenv("OPIK_PROJECT_NAME", "crew_project")

    choices = MODEL_CHOICES if cur_model in MODEL_CHOICES else [cur_model, *MODEL_CHOICES]

    with gr.Tab("5. Configuration", id="settings") as settings_tab:
        settings_header_md = gr.Markdown(
            "### ⚙️ System & Model Configuration\n"
            "Switch between any LLM provider (SovereignEG, Groq, OpenAI, Gemini, OpenRouter, Ollama). "
            "Leave **Base URL** empty when using native providers like `gemini/...` or `openai/...`."
        )

        sec_llm_md = gr.Markdown("#### 🤖 LLM Provider & Model Settings")
        with gr.Row():
            llm_model = gr.Dropdown(
                choices=choices,
                value=cur_model,
                allow_custom_value=True,
                label="Model Name (select or type custom)",
            )
            llm_base_url = gr.Textbox(
                value=cur_base_url,
                placeholder="Leave empty for native providers (e.g. Gemini / OpenAI)",
                label="Base URL (for OpenAI-compatible endpoints)",
            )

        with gr.Row():
            llm_temp = gr.Slider(0.0, 1.0, value=cur_temp, step=0.05, label="Temperature")
            llm_max_tokens = gr.Number(value=cur_max_tokens, precision=0, label="Max Tokens")

        sec_keys_md = gr.Markdown("#### 🔑 API Keys & Opik Project")
        with gr.Row():
            groq_key = gr.Textbox(
                value=cur_groq_key,
                type="password",
                label="Primary LLM API Key (SovereignEG / Groq / OpenAI / etc.)",
            )
            gemini_key = gr.Textbox(
                value=cur_gemini_key,
                type="password",
                label="Gemini API Key (Optional - for Knowledge Embeddings)",
            )

        with gr.Row():
            tavily_key = gr.Textbox(value=cur_tavily_key, type="password", label="Tavily Search API Key (TAVILY_API_KEY)")
            firecrawl_key = gr.Textbox(value=cur_firecrawl_key, type="password", label="Firecrawl API Key (FIRECRAWL_API_KEY)")

        with gr.Row():
            opik_key = gr.Textbox(value=cur_opik_key, type="password", label="Opik Tracing API Key (OPIK_API_KEY)")
            opik_project = gr.Textbox(value=cur_opik_project, label="Opik Project Name")

        save_btn = gr.Button("💾 Save & Apply Settings", variant="primary")
        save_status = gr.Markdown("")

    all_settings = [
        llm_model, llm_base_url, llm_temp, llm_max_tokens,
        groq_key, gemini_key, tavily_key, firecrawl_key, opik_key, opik_project,
    ]

    translatable = {
        "tab_settings": (settings_tab, "tab"),
        "settings_header_md": (settings_header_md, "md"),
        "sec_llm_md": (sec_llm_md, "md"),
        "llm_model": (llm_model, "label"),
        "llm_base_url": (llm_base_url, "label"),
        "llm_temp": (llm_temp, "label"),
        "llm_max_tokens": (llm_max_tokens, "label"),
        "sec_keys_md": (sec_keys_md, "md"),
        "groq_key": (groq_key, "label"),
        "gemini_key": (gemini_key, "label"),
        "tavily_key": (tavily_key, "label"),
        "firecrawl_key": (firecrawl_key, "label"),
        "opik_key": (opik_key, "label"),
        "opik_project": (opik_project, "label"),
        "save_settings_btn": (save_btn, "btn"),
    }

    return {
        "id": "settings",
        "tab": settings_tab,
        "outputs": None,
        "all_settings": all_settings,
        "save_btn": save_btn,
        "save_status": save_status,
        "translatable": translatable,
    }