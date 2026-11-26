import time
from crewai.tools import tool
import crew_project.core.configurations as configurations
from crew_project.crew.tools.tool_monitor import CrewStoppedException, check_stop, log_tool_event


@tool
def search_engine_tool(query: str):
    """Useful for search-based queries. Use this to find current information about any query related pages using a search engine"""
    check_stop()
    t0 = time.perf_counter()
    try:
        # لازم نقرا من الـ module وقت التنفيذ (مش from-import) عشان لما تغيّر الـ key من Settings يشتغل فورًا
        if configurations.tavily_client is None:
            raise RuntimeError("TAVILY_API_KEY is missing. Add it in the Configuration tab and press Save.")
        response = configurations.tavily_client.search(query, max_results=5)
        check_stop()
        raw_results = response.get("results", []) if isinstance(response, dict) else []

        if not raw_results:
            log_tool_event(
                tool_name="Tavily Search",
                target=query,
                status="warning",
                duration_sec=time.perf_counter() - t0,
                message="Search returned 0 results.",
            )
            return {
                "query": query,
                "results": [],
                "directive": "TOOL_WARNING: 0 results found. Move on immediately to the next suggested query. Do NOT invent new queries or URLs.",
            }

        compact_results = [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "score": r.get("score", 0),
                "content": (r.get("content") or "")[:350],
            }
            for r in raw_results
        ]

        log_tool_event(
            tool_name="Tavily Search",
            target=query,
            status="success",
            duration_sec=time.perf_counter() - t0,
            message=f"Found {len(compact_results)} results.",
        )
        return {"query": query, "results": compact_results}

    except CrewStoppedException:
        raise
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
        log_tool_event(
            tool_name="Tavily Search",
            target=query,
            status="error",
            duration_sec=time.perf_counter() - t0,
            message=err,
        )
        return {
            "query": query,
            "error": err,
            "directive": "TOOL_ERROR: Search request failed. Skip this query and move to the next one.",
        }