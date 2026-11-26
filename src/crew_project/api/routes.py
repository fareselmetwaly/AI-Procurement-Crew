import asyncio
import inspect
import json
import os
import threading
from fastapi import APIRouter
from fastapi.responses import FileResponse, PlainTextResponse

from crew_project.api.schemas import ProcurementRequest, RunTriggerResponse
from crew_project.crew.run_crew import run_crew
from crew_project.crew.tools.tool_monitor import request_stop
from crew_project.core.paths import (
    LATEST_CONFIG_PATH,
    METRICS_PATH,
    OUTPUT_DIR,
    REPORT_PATH,
    ROOT_DIR,
    STEP_FILES,
)

router = APIRouter()


def _run_crew_in_background(config: dict, resume_mode: bool = False) -> None:
    os.chdir(ROOT_DIR)
    if inspect.iscoroutinefunction(run_crew):
        asyncio.run(run_crew(config, resume_mode=resume_mode))
    else:
        run_crew(config, resume_mode=resume_mode)


@router.get("/report", tags=["Reports"])
def open_report():
    """يعرض تقرير الـ HTML النهائي في المتصفح."""
    if not REPORT_PATH.exists():
        return PlainTextResponse("No report yet.", status_code=404)
    return FileResponse(str(REPORT_PATH), media_type="text/html")


@router.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": "Procurement Crew"}


@router.get("/api/status", tags=["Crew Execution"])
def get_execution_status():
    """يرجع حالة المراحل اللي خلصت وآخر إحصائيات تشغيل."""
    completed_steps = [
        key for key, filename in STEP_FILES.items()
        if (OUTPUT_DIR / filename).exists()
    ]
    metrics = None
    if METRICS_PATH.exists():
        try:
            metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
        except Exception:
            metrics = None

    return {
        "completed_steps": completed_steps,
        "report_ready": REPORT_PATH.exists(),
        "metrics": metrics,
    }


@router.post("/api/run", response_model=RunTriggerResponse, tags=["Crew Execution"])
def trigger_crew_run(request: ProcurementRequest):
    """يبدأ تشغيل الـ Crew عن طريق الـ API بنفس شروط الـ Validation."""
    config = request.to_run_config()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_CONFIG_PATH.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    threading.Thread(
        target=_run_crew_in_background,
        args=(config, False),
        daemon=True,
    ).start()

    return RunTriggerResponse(
        status="started",
        run_id=config["run_id"],
        message="Procurement crew execution started in background.",
    )


@router.post("/api/stop", tags=["Crew Execution"])
def stop_crew_run():
    """يبعت إشارة إيقاف آمنة للـ Crew."""
    request_stop()
    return {"status": "stopping", "message": "Stop signal sent."}