import json
from pathlib import Path

import gradio as gr
from pydantic import ValidationError

from crew_project.api.schemas import ProcurementRequest, format_validation_error
from crew_project.core.paths import OUTPUT_DIR
from crew_project.ui.config import CURRENCIES, EXAMPLE, EXAMPLE_KEYS, LANGUAGES, STRATEGIES

REQUIRED_INPUT_KEYS = ("company_name", "product_name", "websites_list", "country_name")


def build_template_json_file() -> str:
    """Creates a clean JSON template showing required vs optional fields."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    template_path = OUTPUT_DIR / "procurement_inputs_template.json"
    payload = {
        "_guide": {
            "required_fields": list(REQUIRED_INPUT_KEYS),
            "optional_fields": [k for k in EXAMPLE_KEYS if k not in REQUIRED_INPUT_KEYS],
            "note": "Key order does not matter. Any omitted optional field automatically uses its default.",
        }
    }
    for k in EXAMPLE_KEYS:
        payload[k] = (
            [w.strip() for w in EXAMPLE[k].splitlines() if w.strip()]
            if k == "websites_list"
            else EXAMPLE[k]
        )
    template_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(template_path)


def export_inputs_json(*values) -> str:
    """Exports the current UI form values into a downloadable JSON file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    export_path = OUTPUT_DIR / "exported_procurement_inputs.json"
    payload = {
        "_guide": {
            "required_fields": list(REQUIRED_INPUT_KEYS),
            "optional_fields": [k for k in EXAMPLE_KEYS if k not in REQUIRED_INPUT_KEYS],
        }
    }
    for k, v in zip(EXAMPLE_KEYS, values):
        payload[k] = (
            [w.strip() for w in (v or "").splitlines() if w.strip()]
            if k == "websites_list"
            else v
        )
    export_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(export_path)


def import_inputs_json(file_obj):
    """Reads an uploaded JSON file, validates via Pydantic schema, and populates all 18 UI fields."""
    if file_obj is None:
        return [gr.skip()] * len(EXAMPLE_KEYS)

    file_path = file_obj if isinstance(file_obj, str) else getattr(file_obj, "name", None)
    try:
        raw = json.loads(Path(file_path).read_text(encoding="utf-8"))
    except Exception as e:
        raise gr.Error(f"Invalid JSON file: {e}")

    if not isinstance(raw, dict):
        raise gr.Error("JSON root must be an object { ... }.")

    candidate = {}
    for k in EXAMPLE_KEYS:
        val = raw.get(k, EXAMPLE[k])
        if val is None:
            candidate[k] = None if k == "budget" else EXAMPLE[k]
        elif k == "purchase_strategy":
            candidate[k] = val if val in STRATEGIES else EXAMPLE[k]
        elif k == "currency":
            candidate[k] = val if val in CURRENCIES else EXAMPLE[k]
        elif k == "language":
            candidate[k] = val if val in LANGUAGES else EXAMPLE[k]
        else:
            candidate[k] = val

    try:
        req = ProcurementRequest(**candidate)
    except ValidationError as e:
        raise gr.Error(format_validation_error(e))

    validated = req.model_dump()
    validated["websites_list"] = "\n".join(req.websites_list)

    gr.Info("✅ JSON inputs loaded into their fields!")
    ordered_values = [validated[k] for k in EXAMPLE_KEYS]
    # max_iterations هو آخر عنصر في EXAMPLE_KEYS: نبدّله بـ update عشان يظهر/يختفي حسب use_evaluator
    ordered_values[EXAMPLE_KEYS.index("max_iterations")] = gr.update(
        value=req.max_iterations, visible=bool(req.use_evaluator)
    )
    return ordered_values