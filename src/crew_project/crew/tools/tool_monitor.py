import threading
from datetime import datetime

_LOCK = threading.Lock()
_EVENTS: list[dict] = []
STOP_EVENT = threading.Event()


class CrewStoppedException(Exception):
    """Raised when the user presses Stop to immediately halt execution."""
    pass


def request_stop() -> None:
    """Signals all running tools and crew steps to stop immediately."""
    STOP_EVENT.set()


def clear_stop() -> None:
    """Clears the stop flag at the beginning of a new run or resume."""
    STOP_EVENT.clear()


def is_stop_requested() -> bool:
    return STOP_EVENT.is_set()


def check_stop() -> None:
    """Raises CrewStoppedException if Stop was requested."""
    if STOP_EVENT.is_set():
        raise CrewStoppedException("Execution stopped by user.")


def reset_tool_events() -> None:
    """Clears recorded tool events at the start of every new run."""
    with _LOCK:
        _EVENTS.clear()


def log_tool_event(
    tool_name: str,
    target: str,
    status: str,  # "success" | "warning" | "error"
    duration_sec: float,
    message: str = "",
) -> None:
    """Records a single tool execution outcome for metrics and UI warnings."""
    with _LOCK:
        _EVENTS.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "tool": tool_name,
            "target": target,
            "status": status,
            "duration_sec": round(duration_sec, 2),
            "message": message,
        })


def get_tool_events() -> list[dict]:
    """Returns a snapshot copy of all recorded tool events."""
    with _LOCK:
        return list(_EVENTS)