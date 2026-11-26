import time
from crewai.tools import tool

import crew_project.core.configurations as configurations
from crew_project.crew.tools.tool_monitor import CrewStoppedException, check_stop, log_tool_event
from crew_project.validation.third_agent_val import SingleExtractedProduct


@tool
def web_scraping_tool(page_url: str):
    """
    An AI Tool to help an agent to scrape structured product details from a web page using Firecrawl.

    Example:
    web_scraping_tool(
        page_url="https://www.noon.com/egypt-en/15-bar-fully-automatic-espresso-machine-1-8-l-1500"
    )
    """
    check_stop()
    t0 = time.perf_counter()
    try:
        if configurations.firecrawl_client is None:
            raise RuntimeError("FIRECRAWL_API_KEY is missing or client not initialized.")

        result = configurations.firecrawl_client.scrape(
            page_url,
            formats=[{
                "type": "json",
                "schema": SingleExtractedProduct.model_json_schema(),
            }],
            only_main_content=False,
            timeout=120000,
        )
        check_stop()

        # استخراج البيانات سواء رجعت كـ Pydantic Document أو dict حسب إصدار firecrawl-py
        if isinstance(result, dict):
            extracted = result.get("json") or result.get("extract") or result.get("data", {}).get("json")
            err_msg = result.get("error")
        else:
            extracted = getattr(result, "json", None) or getattr(result, "extract", None)
            err_msg = getattr(result, "error", None)

        if not extracted:
            reason = str(err_msg or "Empty JSON returned by Firecrawl")
            log_tool_event(
                tool_name="Firecrawl",
                target=page_url,
                status="error",
                duration_sec=time.perf_counter() - t0,
                message=reason,
            )
            return {
                "page_url": page_url,
                "error": reason,
                "directive": (
                    "TOOL_ERROR: Failed to extract data from this URL. "
                    "STRICT RULE: Do NOT fabricate, guess, or estimate price or specs for this URL. "
                    "Skip this URL and try another candidate URL from step 2."
                ),
            }

        log_tool_event(
            tool_name="Firecrawl",
            target=page_url,
            status="success",
            duration_sec=time.perf_counter() - t0,
            message="Extracted product details successfully.",
        )
        return {
            "page_url": page_url,
            "details": extracted,
        }

    except CrewStoppedException:
        raise
    except Exception as e:
        err_msg = f"{type(e).__name__}: {e}"
        log_tool_event(
            tool_name="Firecrawl",
            target=page_url,
            status="error",
            duration_sec=time.perf_counter() - t0,
            message=err_msg,
        )
        return {
            "page_url": page_url,
            "error": err_msg,
            "directive": (
                "TOOL_ERROR: Scraping crashed/timed out. "
                "STRICT RULE: Do NOT fabricate data for this URL. Skip it and use another URL."
            ),
        }




# def web_scraping_tool(page_url:str):
#     """
#     An AI Tool to help an agent to scrape a web page

#     Example:
#     web_scraping_tool(
#         page_url="https://www.noon.com/egypt-en/15-bar-fully-automatic-espresso-machine-1-8-l-1500"
#     )
#     """
#     result = scrapegraph_client.extract(
#         url=page_url,
#         prompt="Extract ```json\n" + json.dumps(SingleExtractedProduct.model_json_schema()) + "```\n From the web page",
#         fetch_config=FetchConfig(mode="auto")
#     )

#     if result.status != "success":
#         return {"page_url": page_url, "error": result.error}

#     return {
#         "page_url": page_url,
#         "details": result.data.json_data,
#     }




# print(web_scraping_tool("https://www.noon.com/egypt-ar/home-and-kitchen/home-appliances-31235/small-appliances/coffee-makers/espresso-machines-18741/appliances-deals/"))



# from firecrawl import Firecrawl

# app = Firecrawl(
#   # No API key needed to get started — add one for higher rate limits:
#   # api_key="fc-YOUR-API-KEY",
#   api_key="fc-REDACTED"
# )


# result = app.scrape(
#     'https://www.noon.com/egypt-ar/home-and-kitchen/home-appliances-31235/small-appliances/coffee-makers/espresso-machines-18741/appliances-deals/',
#     formats=[{
#       "type": "json",
#       "schema": SingleExtractedProduct.model_json_schema()
#     }],
#     only_main_content=False,
#     timeout=120000
# )

# print(result)



