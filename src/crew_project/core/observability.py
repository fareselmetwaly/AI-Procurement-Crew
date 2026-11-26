import configparser
import json
import os
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

from crew_project.core.paths import ROOT_DIR

OPIK_DASHBOARD_URL = "https://www.comet.com/opik"


def resolve_crewai_trace_url(root_dir: Path = ROOT_DIR) -> str | None:
    """Reads the latest CrewAI trace URL from .crewai/last_run.json."""
    candidates = [
        root_dir / ".crewai" / "last_run.json",
        root_dir / ".crewai_storage" / "last_run.json",
    ]
    existing = [p for p in candidates if p.exists()]
    if not existing:
        return None

    latest = max(existing, key=lambda p: p.stat().st_mtime)
    try:
        data = json.loads(latest.read_text(encoding="utf-8"))
    except Exception:
        return None

    if isinstance(data, dict):
        for key in ("trace_url", "ephemeral_trace_url", "url", "link"):
            val = data.get(key)
            if isinstance(val, str) and val.startswith("http"):
                return val
        for val in data.values():
            if isinstance(val, str) and val.startswith("http"):
                return val
    return None


@lru_cache(maxsize=16)
def _resolve_opik_ids(api_key: str, project_name: str) -> tuple[str, str]:
    """Fetches (workspace_name, project_id) from Opik API and caches the result."""
    if not api_key:
        return "", ""
    workspace = ""
    project_id = ""
    try:
        import opik
        client = opik.Opik(api_key=api_key, project_name=project_name)
        ws = getattr(client, "_workspace", "") or getattr(getattr(client, "_config", None), "workspace", "")
        if ws and ws.lower() != "default":
            workspace = ws.strip()

        rest = getattr(client, "_rest_client", None)
        if rest:
            if not workspace and hasattr(rest, "workspaces"):
                res = rest.workspaces.get_workspaces()
                names = getattr(res, "workspace_names", None) or []
                if names:
                    workspace = str(names[0]).strip()

            if project_name and hasattr(rest, "projects"):
                proj_res = rest.projects.find_projects(name=project_name)
                content = getattr(proj_res, "content", None) or []
                for p in content:
                    if getattr(p, "name", "") == project_name and getattr(p, "id", ""):
                        project_id = str(p.id).strip()
                        break
    except Exception:
        pass
    return workspace, project_id


def resolve_opik_project_url(project_name: str, default_url: str = OPIK_DASHBOARD_URL) -> str:
    """Resolves the direct Opik project traces URL for the active project_name."""
    workspace = os.getenv("OPIK_WORKSPACE", "").strip()
    base_ui = default_url.rstrip("/")

    opik_cfg_file = Path.home() / ".opik.config"
    if opik_cfg_file.exists():
        try:
            cp = configparser.ConfigParser()
            cp.read(opik_cfg_file, encoding="utf-8")
            if cp.has_section("opik"):
                if not workspace:
                    workspace = cp.get("opik", "workspace", fallback="").strip()
                url_override = cp.get("opik", "url_override", fallback="").strip()
                if url_override:
                    cleaned = url_override.rstrip("/")
                    if cleaned.endswith("/api"):
                        cleaned = cleaned[:-4]
                    base_ui = cleaned.rstrip("/")
        except Exception:
            pass

    if not workspace or workspace.lower() == "default":
        try:
            from opik.config import OpikConfig
            cfg = OpikConfig()
            cfg_ws = (getattr(cfg, "workspace", "") or "").strip()
            if cfg_ws and cfg_ws.lower() != "default":
                workspace = cfg_ws
        except Exception:
            pass

    api_key = os.getenv("OPIK_API_KEY", "").strip()
    fetched_ws, project_id = _resolve_opik_ids(api_key, (project_name or "").strip())
    if (not workspace or workspace.lower() == "default") and fetched_ws:
        workspace = fetched_ws

    if workspace and project_id:
        return f"{base_ui}/{quote(workspace)}/projects/{quote(project_id)}/traces"
    if workspace:
        return f"{base_ui}/{quote(workspace)}/projects"
    return base_ui