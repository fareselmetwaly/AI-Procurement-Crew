import gradio as gr

EYE_COMFORT_CSS = """
:root {
    --pc-bg: #f4f6f9;
    --pc-card-bg: #ffffff;
    --pc-surface-alt: #eef2f6;
    --pc-border: #dce2ec;
    --pc-text: #1e293b;
    --pc-muted: #526075;
    --pc-accent: #4f46e5;
    --pc-accent-soft: rgba(79, 70, 229, 0.10);
    --pc-success: #15803d;
    --pc-success-soft: rgba(22, 163, 74, 0.12);
    --pc-warn: #b45309;
    --pc-warn-soft: rgba(217, 119, 6, 0.12);
    --pc-danger: #b91c1c;
    --pc-danger-soft: rgba(220, 38, 38, 0.12);
}

.dark {
    --pc-bg: #0f172a;
    --pc-card-bg: #1e293b;
    --pc-surface-alt: #162033;
    --pc-border: #334155;
    --pc-text: #e2e8f0;
    --pc-muted: #94a3b8;
    --pc-accent: #818cf8;
    --pc-accent-soft: rgba(129, 140, 248, 0.15);
    --pc-success: #34d399;
    --pc-success-soft: rgba(52, 211, 153, 0.14);
    --pc-warn: #fbbf24;
    --pc-warn-soft: rgba(251, 191, 36, 0.14);
    --pc-danger: #f87171;
    --pc-danger-soft: rgba(248, 113, 113, 0.15);
}

body, .gradio-container {
    background-color: var(--pc-bg) !important;
    color: var(--pc-text) !important;
}

footer { display: none !important; }

.pc-card {
    background: var(--pc-card-bg);
    border: 1px solid var(--pc-border);
    border-radius: 10px;
    padding: 12px 14px;
    color: var(--pc-text);
}

.pc-empty {
    padding: 16px;
    border: 1px dashed var(--pc-border);
    border-radius: 10px;
    color: var(--pc-muted);
    background: var(--pc-surface-alt);
    text-align: center;
    font-size: 13.5px;
}

.pc-muted { color: var(--pc-muted); }
.pc-accent-text { color: var(--pc-accent); }
.pc-success-text { color: var(--pc-success); }
.pc-warn-text { color: var(--pc-warn); }

.pc-badge {
    display: inline-block;
    padding: 2px 9px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    margin: 2px;
}
.pc-badge-info { background: var(--pc-accent-soft); color: var(--pc-accent); }
.pc-badge-success { background: var(--pc-success-soft); color: var(--pc-success); }
.pc-badge-warn { background: var(--pc-warn-soft); color: var(--pc-warn); }
.pc-badge-danger { background: var(--pc-danger-soft); color: var(--pc-danger); }

.pc-pill-num {
    background: var(--pc-accent-soft);
    color: var(--pc-accent);
    font-weight: 700;
    font-size: 11.5px;
    padding: 2px 8px;
    border-radius: 999px;
}

.pc-link {
    color: var(--pc-accent);
    font-weight: 600;
    text-decoration: none;
}
.pc-link:hover { text-decoration: underline; }

.pc-btn-link {
    display: block;
    width: 100%;
    text-align: center;
    padding: 8px 14px;
    background: var(--pc-accent);
    color: #ffffff !important;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    font-size: 13px;
}

.pc-price {
    font-size: 16.5px;
    font-weight: 700;
    color: var(--pc-success);
    margin-bottom: 10px;
}

.pc-prod-img {
    width: 100%;
    height: 145px;
    object-fit: contain;
    background: #f8fafc;
    border: 1px solid var(--pc-border);
    border-radius: 8px;
    padding: 6px;
    margin-bottom: 10px;
}

.pc-table-wrap {
    overflow-x: auto;
    border: 1px solid var(--pc-border);
    border-radius: 10px;
    background: var(--pc-card-bg);
}

.pc-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13.5px;
    color: var(--pc-text);
}

.pc-table thead tr {
    background: var(--pc-surface-alt);
    text-align: left;
}

.pc-table th {
    padding: 10px;
    border-bottom: 1px solid var(--pc-border);
}

.pc-tr {
    border-bottom: 1px solid var(--pc-border);
}

.pc-warn-box {
    margin: 14px 0;
    padding: 12px 16px;
    border-radius: 10px;
    background: var(--pc-warn-soft);
    border: 1px solid var(--pc-warn);
}

.pc-bar-bg {
    height: 6px;
    background: var(--pc-surface-alt);
    border-radius: 4px;
    margin-top: 4px;
}
.pc-bar-time {
    height: 100%;
    background: var(--pc-accent);
    border-radius: 4px;
}
.pc-bar-tok {
    height: 100%;
    background: var(--pc-success);
    border-radius: 4px;
}
"""

EYE_COMFORT_THEME = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="slate",
    neutral_hue="slate",
)

TOGGLE_THEME_JS = """
() => {
    const isDark = !document.body.classList.contains('dark');
    [document.body, document.documentElement, document.querySelector('gradio-app')].forEach(el => {
        if (el) el.classList.toggle('dark', isDark);
    });
    document.documentElement.style.colorScheme = isDark ? 'dark' : 'light';
    localStorage.setItem('crew_ui_theme', isDark ? 'dark' : 'light');
    return isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
}
"""

LOAD_THEME_JS = """
() => {
    const isDark = localStorage.getItem('crew_ui_theme') === 'dark';
    [document.body, document.documentElement, document.querySelector('gradio-app')].forEach(el => {
        if (el) el.classList.toggle('dark', isDark);
    });
    document.documentElement.style.colorScheme = isDark ? 'dark' : 'light';
    return isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
}
"""