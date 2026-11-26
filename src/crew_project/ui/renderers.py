import html
from typing import Any


def _esc(val: Any) -> str:
    return html.escape("" if val is None else str(val), quote=True)


def render_empty_box(msg: str) -> str:
    return f'<div class="pc-empty">{_esc(msg)}</div>'


def render_inputs_card(config: dict | None) -> str:
    if not config:
        return render_empty_box("Waiting for inputs...")

    budget_val = f"{config.get('budget')} {config.get('currency', '')}" if config.get("budget") else "Flexible"
    websites = config.get("websites_list") or []
    sites_badges = "".join(
        f'<span class="pc-badge pc-badge-info">{_esc(w)}</span>'
        for w in websites
    )
    boycott = "Enabled" if config.get("exclude_israeli_supported") else "Disabled"
    evaluator = f"Enabled ({config.get('max_iterations', 0)}x)" if config.get("use_evaluator") else "Disabled"

    items = [
        ("🏢 Company", config.get("company_name", "-")),
        ("📦 Product", config.get("product_name", "-")),
        ("🎯 Strategy", config.get("purchase_strategy", "-")),
        ("💰 Budget", budget_val),
        ("🔢 Quantity", f"{config.get('quantity', 1)} ({config.get('currency', 'EGP')})"),
        ("🌍 Country / Lang", f"{config.get('country_name', '-')} / {config.get('language', '-')}"),
        ("🔍 Queries / Top N", f"{config.get('no_keywords', 10)} queries / Top {config.get('top_recommendations_no', 10)}"),
        ("🛡️ Boycott Filter", boycott),
        ("🔁 Evaluator", evaluator),
        ("📅 Date / Run ID", f"{config.get('current_date', '-')} | {config.get('run_id', '-')}"),
    ]

    cards = "".join(
        f'<div class="pc-card">'
        f'<div class="pc-muted" style="font-size:11.5px;margin-bottom:3px;">{_esc(k)}</div>'
        f'<div style="font-weight:600;font-size:13.5px;">{_esc(v)}</div>'
        f"</div>"
        for k, v in items
    )

    extra_html = ""
    if config.get("important_specs") or config.get("extra_requirements"):
        extra_html = (
            f'<div class="pc-card" style="margin-top:10px;font-size:13px;">'
            f'<div><b>Specs:</b> {_esc(config.get("important_specs") or "—")}</div>'
            f'<div style="margin-top:4px;"><b>Extra:</b> {_esc(config.get("extra_requirements") or "—")}</div>'
            f"</div>"
        )

    return (
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">'
        f"{cards}</div>"
        f'<div style="margin-top:10px;font-size:13px;"><b>Target Websites:</b> {sites_badges}</div>'
        f"{extra_html}"
    )


def render_queries_cards(queries_data: dict | None) -> str:
    if not queries_data:
        return render_empty_box("Waiting for Search Queries Agent...")

    queries = queries_data.get("queries") if isinstance(queries_data, dict) else []
    if not queries:
        return render_empty_box("No search queries generated.")

    pills = "".join(
        f'<div class="pc-card" style="display:flex;align-items:center;gap:8px;padding:9px 12px;font-size:13.5px;">'
        f'<span class="pc-pill-num">#{idx}</span>'
        f'<span>{_esc(q)}</span>'
        f"</div>"
        for idx, q in enumerate(queries, start=1)
    )
    return (
        f'<div class="pc-muted" style="margin-bottom:8px;font-size:13px;">'
        f'Generated <b>{len(queries)}</b> targeted search queries:</div>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:8px;">'
        f"{pills}</div>"
    )


def render_search_results(search_data: dict | None) -> str:
    if not search_data:
        return render_empty_box("Waiting for Search Engine Agent...")

    results = search_data.get("results") if isinstance(search_data, dict) else []
    if not results:
        return render_empty_box("No search results returned.")

    rows = []
    for idx, r in enumerate(results, start=1):
        title = _esc(r.get("title") or "Untitled Page")
        url = _esc(r.get("url") or "#")
        score = float(r.get("score") or 0)
        q_text = _esc(r.get("search_query") or "")
        snippet = _esc((r.get("content") or "")[:180])
        badge_cls = "pc-badge-success" if score >= 0.5 else "pc-badge-warn"

        rows.append(
            f'<tr class="pc-tr">'
            f'<td style="padding:10px;font-weight:600;vertical-align:top;">{idx}</td>'
            f'<td style="padding:10px;vertical-align:top;">'
            f'<a href="{url}" target="_blank" class="pc-link">{title} ↗</a>'
            f'<div class="pc-muted" style="font-size:12px;margin-top:4px;">{snippet}...</div>'
            f'<div class="pc-accent-text" style="font-size:11.5px;margin-top:4px;">Query: {q_text}</div>'
            f"</td>"
            f'<td style="padding:10px;text-align:center;vertical-align:top;">'
            f'<span class="pc-badge {badge_cls}">{score:.2f}</span>'
            f"</td>"
            f"</tr>"
        )

    return (
        f'<div class="pc-muted" style="margin-bottom:8px;font-size:13px;">'
        f'Found <b>{len(results)}</b> candidate product links:</div>'
        f'<div class="pc-table-wrap">'
        f'<table class="pc-table">'
        f'<thead><tr>'
        f'<th style="width:40px;">#</th>'
        f'<th>Product Page & Snippet</th>'
        f'<th style="width:90px;text-align:center;">Score</th>'
        f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
    )


def render_products_grid(products_data: dict | None) -> str:
    if not products_data:
        return render_empty_box("Waiting for Web Scraping Agent...")

    products = products_data.get("products") if isinstance(products_data, dict) else []
    if not products:
        return render_empty_box("No valid products extracted.")

    cards = []
    for p in products:
        title = _esc(p.get("product_title") or "Unnamed Product")
        url = _esc(p.get("product_url") or p.get("page_url") or "#")
        img = _esc(p.get("product_image_url") or "")
        cur_price = _esc(p.get("product_current_price") or "N/A")
        orig_price = p.get("product_original_price")
        disc = p.get("product_discount_percentage")
        rank = int(p.get("agent_recommendation_rank") or 0)
        specs = p.get("product_specs") or []
        notes = p.get("agent_recommendation_notes") or []

        orig_html = (
            f'<span class="pc-muted" style="text-decoration:line-through;font-size:13px;margin-left:6px;">{_esc(orig_price)}</span>'
            if orig_price else ""
        )
        disc_html = (
            f'<span class="pc-badge pc-badge-danger">-{_esc(disc)}%</span>'
            if disc else ""
        )

        specs_rows = "".join(
            f'<li style="margin-bottom:2px;"><b>{_esc(s.get("specification_name"))}:</b> {_esc(s.get("specification_value"))}</li>'
            for s in specs[:5]
        )
        notes_rows = "".join(
            f'<li style="margin-bottom:2px;">{_esc(n)}</li>'
            for n in notes[:3]
        )

        img_block = (
            f'<img src="{img}" alt="{title}" onerror="this.remove()" class="pc-prod-img" />'
            if img.startswith("http") else ""
        )

        cards.append(
            f'<div class="pc-card" style="display:flex;flex-direction:column;justify-content:space-between;">'
            f"<div>"
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">'
            f'<span class="pc-badge pc-badge-warn">⭐ Rank {rank}/5</span>'
            f"{disc_html}"
            f"</div>"
            f"{img_block}"
            f'<div style="font-weight:700;font-size:14.5px;line-height:1.4;margin-bottom:8px;">{title}</div>'
            f'<div class="pc-price">{cur_price}{orig_html}</div>'
            f'<div style="font-size:12.5px;margin-bottom:8px;"><b>Specifications:</b>'
            f'<ul style="margin:4px 0 0 16px;padding:0;">{specs_rows or "<li>—</li>"}</ul></div>'
            f'<div class="pc-muted" style="font-size:12px;"><b>Agent Notes:</b>'
            f'<ul style="margin:4px 0 0 16px;padding:0;">{notes_rows or "<li>—</li>"}</ul></div>'
            f"</div>"
            f'<a href="{url}" target="_blank" class="pc-btn-link" style="margin-top:12px;">'
            f"Open Store Page ↗</a>"
            f"</div>"
        )

    return (
        f'<div class="pc-muted" style="margin-bottom:10px;font-size:13px;">'
        f'Extracted <b>{len(products)}</b> verified products:</div>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:14px;">'
        f"{''.join(cards)}</div>"
    )


def render_report_iframe(report_html: str | None) -> str:
    if not report_html or not report_html.strip():
        return render_empty_box("No report generated yet. Run the crew first to preview the report here.")

    escaped_doc = html.escape(report_html, quote=True)
    return (
        f'<iframe srcdoc="{escaped_doc}" '
        f'style="width:100%;height:780px;border:1px solid var(--pc-border);'
        f'border-radius:12px;background:#f8fafc;" sandbox="allow-same-origin allow-popups"></iframe>'
    )

def render_metrics_dashboard(
    metrics: dict | None,
    opik_url: str = "https://www.comet.com/opik",
    opik_project: str = "crew_project",
    crewai_trace_url: str | None = None,
) -> str:
    crewai_action = (
        f'<a href="{_esc(crewai_trace_url)}" target="_blank" class="pc-btn-link" style="width:auto;padding:7px 14px;">Open CrewAI Trace ↗</a>'
        if crewai_trace_url
        else '<span class="pc-muted" style="font-size:12.5px;">Waiting for last_run.json trace...</span>'
    )

    tracing_banners = (
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px;margin-bottom:14px;">'
        f'<div class="pc-card" style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px;">'
        f'<div><b>🔭 Opik Project:</b> <code>{_esc(opik_project)}</code></div>'
        f'<a href="{_esc(opik_url)}" target="_blank" class="pc-btn-link" style="width:auto;padding:7px 14px;">Open Opik Project ↗</a>'
        f"</div>"
        f'<div class="pc-card" style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px;">'
        f'<div><b>🧵 CrewAI Trace:</b> <code>.crewai/last_run.json</code></div>'
        f"{crewai_action}"
        f"</div>"
        f"</div>"
    )

    if not metrics:
        return tracing_banners + render_empty_box("No metrics recorded yet. Complete a run to view per-agent tokens, duration, and tool traces.")

    totals = metrics.get("totals") or {}
    agents = metrics.get("agents") or []
    warnings = metrics.get("warnings") or []
    tool_events = metrics.get("tool_events") or []
    w_count = int(metrics.get("warnings_count") or len(warnings))

    status_badge = f"⚠️ {w_count} Warning(s)" if w_count > 0 else "✅ Clean Success"
    status_cls = "pc-warn-text" if w_count > 0 else "pc-success-text"

    kpis = [
        ("Run Status", status_badge, status_cls),
        ("Total Duration", f"{totals.get('total_duration_sec', 0)} s", "pc-accent-text"),
        ("Total Tokens", f"{totals.get('total_tokens', 0):,}", "pc-accent-text"),
        ("Input / Output Tokens", f"{totals.get('prompt_tokens', 0):,} / {totals.get('completion_tokens', 0):,}", ""),
        ("Total LLM Calls", str(totals.get("llm_calls", 0)), ""),
    ]

    kpi_cards = "".join(
        f'<div class="pc-card">'
        f'<div class="pc-muted" style="font-size:12px;">{_esc(label)}</div>'
        f'<div class="{cls}" style="font-size:17px;font-weight:700;margin-top:4px;">{_esc(val)}</div>'
        f"</div>"
        for label, val, cls in kpis
    )

    warnings_html = ""
    if warnings:
        w_items = "".join(
            f'<li style="margin-bottom:5px;"><b>[{_esc(w.get("timestamp"))}] {_esc(w.get("tool"))}</b> '
            f'({_esc(w.get("target"))}): <span class="pc-warn-text">{_esc(w.get("message"))}</span></li>'
            for w in warnings
        )
        warnings_html = (
            f'<div class="pc-warn-box">'
            f'<div class="pc-warn-text" style="font-weight:700;margin-bottom:6px;">⚠️ Tool Warnings & Failed Scrapes ({len(warnings)})</div>'
            f'<ul style="margin:0 0 0 18px;padding:0;font-size:13px;">{w_items}</ul>'
            f"</div>"
        )

    max_tok = max([a.get("total_tokens", 0) for a in agents] + [1])
    max_sec = max([a.get("duration_sec", 0) for a in agents] + [0.1])
    agent_rows = []
    for a in agents:
        tok = a.get("total_tokens", 0)
        sec = a.get("duration_sec", 0)
        tok_pct = min(100, int((tok / max_tok) * 100))
        sec_pct = min(100, int((sec / max_sec) * 100))
        agent_rows.append(
            f'<tr class="pc-tr">'
            f'<td style="padding:10px;font-weight:700;">Step {a.get("step")}</td>'
            f'<td style="padding:10px;font-weight:600;">{_esc(a.get("agent"))}</td>'
            f'<td style="padding:10px;">{sec} s'
            f'<div class="pc-bar-bg"><div class="pc-bar-time" style="width:{sec_pct}%;"></div></div></td>'
            f'<td style="padding:10px;">{a.get("prompt_tokens", 0):,}</td>'
            f'<td style="padding:10px;">{a.get("completion_tokens", 0):,}</td>'
            f'<td style="padding:10px;font-weight:700;">{tok:,}'
            f'<div class="pc-bar-bg"><div class="pc-bar-tok" style="width:{tok_pct}%;"></div></div></td>'
            f'<td style="padding:10px;text-align:center;">{a.get("llm_calls", 0)}</td>'
            f"</tr>"
        )

    agents_table = (
        f'<h4 style="margin:16px 0 8px;">⏱️ Per-Agent Time & Token Consumption</h4>'
        f'<div class="pc-table-wrap">'
        f'<table class="pc-table">'
        f'<thead><tr>'
        f'<th>Step</th><th>Agent</th><th>Duration</th><th>Input Tokens</th>'
        f'<th>Output Tokens</th><th>Total Tokens</th><th style="text-align:center;">LLM Calls</th>'
        f'</tr></thead><tbody>{"".join(agent_rows) or "<tr><td colspan=7 style=padding:12px;>No per-agent data.</td></tr>"}</tbody></table></div>'
    )

    trace_rows = []
    for ev in tool_events:
        st = ev.get("status", "success")
        st_badge = (
            '<span class="pc-badge pc-badge-success">SUCCESS</span>'
            if st == "success"
            else '<span class="pc-badge pc-badge-warn">' + _esc(st.upper()) + "</span>"
        )
        trace_rows.append(
            f'<tr class="pc-tr">'
            f'<td style="padding:8px 10px;font-size:12px;">{_esc(ev.get("timestamp"))}</td>'
            f'<td style="padding:8px 10px;font-weight:600;">{_esc(ev.get("tool"))}</td>'
            f'<td style="padding:8px 10px;max-width:320px;word-break:break-all;font-size:12.5px;">{_esc(ev.get("target"))}</td>'
            f'<td style="padding:8px 10px;">{_esc(ev.get("duration_sec"))} s</td>'
            f'<td style="padding:8px 10px;">{st_badge}</td>'
            f'<td style="padding:8px 10px;font-size:12.5px;">{_esc(ev.get("message"))}</td>'
            f"</tr>"
        )

    trace_table = (
        f'<h4 style="margin:18px 0 8px;">🛠️ CrewAI Tool Execution Trace ({len(tool_events)} calls)</h4>'
        f'<div class="pc-table-wrap">'
        f'<table class="pc-table">'
        f'<thead><tr>'
        f'<th>Time</th><th>Tool</th><th>Query / URL</th><th>Duration</th>'
        f'<th>Status</th><th>Outcome</th>'
        f'</tr></thead><tbody>{"".join(trace_rows) or "<tr><td colspan=6 style=padding:12px;>No tool calls recorded.</td></tr>"}</tbody></table></div>'
    )

    return (
        f"{tracing_banners}"
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(175px,1fr));gap:10px;">{kpi_cards}</div>'
        f"{warnings_html}"
        f"{agents_table}"
        f"{trace_table}"
    )


def render_progress_report_link(report_ready: bool) -> str:
    if not report_ready:
        return "<i>Report not ready yet...</i>"
    return '<a href="/report" target="_blank" class="pc-link">🔗 Open report in a new tab</a>'


def render_full_report_button(
    report_ready: bool,
    empty_msg: str = "Generating report...",
) -> str:
    if not report_ready:
        return f"<i>{_esc(empty_msg)}</i>"
    return (
        '<a href="/report" target="_blank" class="pc-btn-link" '
        'style="display:inline-block;width:auto;">'
        "🔗 Open Full Report in New Tab (Print / Save as PDF)</a>"
    )