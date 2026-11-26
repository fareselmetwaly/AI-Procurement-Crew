# كل key هنا لازم يكون موجود في "en" و "ar".
# الـ keys دي هي نفسها اللي بتتسجل في `translatable` جوه ملفات ui/tabs/*.py
# والـ "en" لازم يطابق الـ label الأصلي اللي مكتوب في الـ tab، عشان لما ترجع للإنجليزي الشكل يبقى زي ما كان.
# لو ضفت component جديد في translatable ضيف الـ key بتاعه هنا (في اللغتين) — في فحص تلقائي في ui/app.py بيقولك لو نسيت.

TEXTS = {
    "en": {
        # --- Header ---
        "header_md": (
            "# 🛒 Procurement Crew\n"
            "AI agents that search the web, scrape product pages, compare prices and write an executive procurement report."
        ),
        "lang_btn": "🌐 العربية",

        # --- Tab titles ---
        "tab_inputs": "1. Inputs",
        "tab_progress": "2. Progress",
        "tab_report": "3. Final Report",
        "tab_obs": "4. Observability & Metrics",
        "tab_settings": "5. Configuration",

        # --- Inputs tab ---
        "basics_md": "### Basics",
        "company_name": "Company name",
        "product_name": "Product *",
        "websites_list": "Websites (one per line) *",
        "country_name": "Country",
        "purchase_strategy": "Purchase strategy",
        "acc_company": "Company details",
        "about_company": "About the company",
        "acc_request": "Request details",
        "budget": "Budget (optional)",
        "quantity": "Quantity",
        "currency": "Currency",
        "extra_requirements": "Extra requirements (optional)",
        "important_specs": "Important specs (optional)",
        "acc_search": "Search & filtering",
        "language": "Search keywords language",
        "no_keywords": "Number of search queries",
        "score_th": "Min search score (Tavily)",
        "top_recommendations_no": "Number of products to extract",
        "exclude_israeli_supported": "Exclude products/companies that support Israel (The Wall filter)",
        "acc_evaluator": "Evaluator (optional)",
        "use_evaluator": "Enable Evaluator-Optimizer loop",
        "max_iterations": "Max iterations",
        "example_btn": "Load example",
        "resume_btn": "▶️ Resume Last Step",
        "run_btn": "Run",

        # --- Progress tab ---
        "stop_btn": "⏹️ Stop Execution",
        "acc_p0": "0. Inputs (Request Summary)",
        "acc_p1": "1. Search Queries Agent",
        "acc_p2": "2. Search Engine Agent",
        "acc_p3": "3. Web Scraping Agent",
        "acc_p4": "4. Report Author Agent",
        "report_file": "Download report (HTML)",

        # --- Report tab ---
        "report_header_md": (
            "### 📄 Executive Procurement Report\n"
            "Preview the generated report below, open it in a full browser tab, or download it."
        ),
        "report_download": "Download Report (HTML)",

        # --- Observability tab ---
        "obs_header_md": "### 📊 Observability, Token Metrics & CrewAI Tracing",
        "refresh_metrics_btn": "🔄 Refresh Metrics",

        # --- Settings tab ---
        "settings_header_md": "### ⚙️ System & Model Configuration\nSwitch between any LLM provider (SovereignEG, Groq, OpenAI, Gemini, OpenRouter, Ollama). Leave **Base URL** empty when using native providers like `gemini/...` or `openai/...`.",
        "sec_llm_md": "#### 🤖 LLM Provider & Model Settings",
        "llm_model": "Model Name (select or type custom)",
        "llm_base_url": "Base URL (for OpenAI-compatible endpoints)",
        "llm_temp": "Temperature",
        "llm_max_tokens": "Max Tokens",
        "sec_keys_md": "#### 🔑 API Keys & Opik Project",
        "groq_key": "Primary LLM API Key (SovereignEG / Groq / OpenAI / etc.)",
        "gemini_key": "Gemini API Key (Optional - for Knowledge Embeddings)",
        "tavily_key": "Tavily Search API Key (TAVILY_API_KEY)",
        "firecrawl_key": "Firecrawl API Key (FIRECRAWL_API_KEY)",
        "opik_key": "Opik Tracing API Key (OPIK_API_KEY)",
        "opik_project": "Opik Project Name",
        "save_settings_btn": "💾 Save & Apply Settings",
    },
    "ar": {
        # --- Header ---
        "header_md": (
            "# 🛒 فريق المشتريات الذكي\n"
            "وكلاء ذكاء اصطناعي يبحثون في الويب ويستخرجون بيانات المنتجات ويقارنون الأسعار ويكتبون تقرير مشتريات تنفيذي."
        ),
        "lang_btn": "🌐 English",

        # --- Tab titles ---
        "tab_inputs": "1. المدخلات",
        "tab_progress": "2. التقدم",
        "tab_report": "3. التقرير النهائي",
        "tab_obs": "4. المراقبة والإحصائيات",
        "tab_settings": "5. الإعدادات",

        # --- Inputs tab ---
        "basics_md": "### الأساسيات",
        "company_name": "اسم الشركة",
        "product_name": "المنتج المطلوب *",
        "websites_list": "المواقع المستهدفة (موقع في كل سطر) *",
        "country_name": "الدولة",
        "purchase_strategy": "استراتيجية الشراء",
        "acc_company": "بيانات الشركة",
        "about_company": "نبذة عن الشركة ومجال العمل",
        "acc_request": "تفاصيل الطلب",
        "budget": "الميزانية (اختياري)",
        "quantity": "الكمية",
        "currency": "العملة",
        "extra_requirements": "متطلبات إضافية (اختياري)",
        "important_specs": "المواصفات المهمة (اختياري)",
        "acc_search": "البحث والفلترة",
        "language": "لغة جمل البحث",
        "no_keywords": "عدد جمل البحث",
        "score_th": "أقل درجة صلة للبحث (Tavily)",
        "top_recommendations_no": "عدد المنتجات المطلوب استخراجها",
        "exclude_israeli_supported": "استبعاد المنتجات والشركات الداعمة للاحتلال (فلتر The Wall)",
        "acc_evaluator": "المراجع الآلي (اختياري)",
        "use_evaluator": "تفعيل حلقة المراجعة والتحسين (Evaluator-Optimizer)",
        "max_iterations": "أقصى عدد مرات المراجعة",
        "example_btn": "تحميل مثال",
        "resume_btn": "▶️ استكمال من آخر خطوة",
        "run_btn": "تشغيل",

        # --- Progress tab ---
        "stop_btn": "⏹️ إيقاف التشغيل",
        "acc_p0": "0. المدخلات (ملخص الطلب)",
        "acc_p1": "1. وكيل جمل البحث",
        "acc_p2": "2. وكيل محرك البحث",
        "acc_p3": "3. وكيل استخراج البيانات",
        "acc_p4": "4. وكيل كتابة التقرير",
        "report_file": "تحميل التقرير (HTML)",

        # --- Report tab ---
        "report_header_md": (
            "### 📄 تقرير المشتريات التنفيذي\n"
            "شاهد التقرير بالأسفل، أو افتحه في تبويب كامل، أو حمّله."
        ),
        "report_download": "تحميل التقرير (HTML)",

        # --- Observability tab ---
        "obs_header_md": "### 📊 المراقبة، إحصائيات التوكنز وتتبع CrewAI",
        "refresh_metrics_btn": "🔄 تحديث الإحصائيات",

        # --- Settings tab ---
        "settings_header_md": "### ⚙️ إعدادات النظام والموديل\nيمكنك التبديل بين أي منصة ذكاء اصطناعي (SovereignEG, Groq, OpenAI, Gemini, OpenRouter, Ollama). اترك **Base URL** فارغاً عند استخدام المنصات الرسمية مثل `gemini/...` أو `openai/...`.",
        "sec_llm_md": "#### 🤖 إعدادات المنصة والموديل (LLM)",
        "llm_model": "اسم الموديل (اختر من القائمة أو اكتب اسماً جديداً)",
        "llm_base_url": "رابط الخادم (Base URL - للمنصات المتوافقة مع OpenAI)",
        "llm_temp": "درجة الإبداع (Temperature)",
        "llm_max_tokens": "الحد الأقصى للتوكنز (Max Tokens)",
        "sec_keys_md": "#### 🔑 مفاتيح الربط (API Keys) و Opik",
        "groq_key": "مفتاح الموديل الأساسي (SovereignEG / Groq / OpenAI / إلخ)",
        "gemini_key": "مفتاح Gemini للـ Embeddings (اختياري)",
        "tavily_key": "مفتاح البحث (TAVILY_API_KEY)",
        "firecrawl_key": "مفتاح استخراج البيانات (FIRECRAWL_API_KEY)",
        "opik_key": "مفتاح التتبع (OPIK_API_KEY)",
        "opik_project": "اسم المشروع في Opik",
        "save_settings_btn": "💾 حفظ وتطبيق الإعدادات",
    },
}
