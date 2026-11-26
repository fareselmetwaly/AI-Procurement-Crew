import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field, ValidationError, field_validator


class ProcurementRequest(BaseModel):
    """Schema موحدة للتحقق من مدخلات طلب الشراء سواء جاية من Gradio أو FastAPI."""

    company_name: str = Field(..., min_length=1, description="اسم الشركة")
    about_company: str = Field(default="", description="نبذة عن الشركة")
    product_name: str = Field(..., min_length=1, description="اسم المنتج المطلوب")
    purchase_strategy: str = Field(default="Value for price")
    budget: float | None = Field(default=None, ge=0, description="الميزانية اختيارية ولا تقبل السالب")
    quantity: int = Field(default=1, ge=1, description="الكمية لا تقل عن 1")
    currency: str = Field(default="EGP")
    extra_requirements: str = Field(default="")
    important_specs: str = Field(default="")
    websites_list: list[str] = Field(..., min_length=1, description="قائمة المواقع المستهدفة")
    country_name: str = Field(..., min_length=1, description="الدولة")
    language: str = Field(default="English")
    no_keywords: int = Field(default=10, ge=1, le=20)
    score_th: float = Field(default=0.10, ge=0.0, le=1.0)
    top_recommendations_no: int = Field(default=10, ge=1, le=30)
    exclude_israeli_supported: bool = Field(default=True)
    use_evaluator: bool = Field(default=False)
    max_iterations: int = Field(default=2, ge=0, le=5)

    @field_validator("company_name", "product_name", "country_name", mode="before")
    @classmethod
    def _strip_and_require_text(cls, v: Any, info) -> str:
        text = (str(v) if v is not None else "").strip()
        if not text:
            labels = {
                "company_name": "Company name",
                "product_name": "Product name",
                "country_name": "Country",
            }
            raise ValueError(f"{labels.get(info.field_name, info.field_name)} is required.")
        return text

    @field_validator("about_company", "extra_requirements", "important_specs", mode="before")
    @classmethod
    def _strip_optional_text(cls, v: Any) -> str:
        return (str(v) if v is not None else "").strip()

    @field_validator("budget", mode="before")
    @classmethod
    def _normalize_budget(cls, v: Any) -> float | None:
        if v is None or v == "" or v == 0:
            return None
        val = float(v)
        if val < 0:
            raise ValueError("Budget cannot be negative.")
        return val

    @field_validator("websites_list", mode="before")
    @classmethod
    def _parse_websites(cls, v: Any) -> list[str]:
        # يقبل قائمة جاهزة (من JSON/API) أو نص مقسوم بسطور (من Gradio)
        if isinstance(v, str):
            sites = [w.strip() for w in v.splitlines() if w.strip()]
        elif isinstance(v, list):
            sites = [str(w).strip() for w in v if str(w).strip()]
        else:
            sites = []

        if not sites:
            raise ValueError("Add at least one website (one per line).")
        return sites

    def to_run_config(self) -> dict[str, Any]:
        """يحول الـ Schema لنفس قاموس التشغيل اللي run_crew مستنيه بالظبط."""
        return {
            "company_name": self.company_name,
            "about_company": self.about_company,
            "product_name": self.product_name,
            "purchase_strategy": self.purchase_strategy,
            "budget": self.budget,
            "quantity": self.quantity,
            "currency": self.currency,
            "extra_requirements": self.extra_requirements,
            "important_specs": self.important_specs,
            "websites_list": self.websites_list,
            "country_name": self.country_name,
            "language": self.language,
            "no_keywords": self.no_keywords,
            "score_th": self.score_th,
            "top_recommendations_no": self.top_recommendations_no,
            "exclude_israeli_supported": self.exclude_israeli_supported,
            "use_evaluator": self.use_evaluator,
            "max_iterations": self.max_iterations if self.use_evaluator else 0,
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            "run_id": datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:6],
        }


class RuntimeSettingsRequest(BaseModel):
    """Schema للتحقق من إعدادات الموديل ومفاتيح الـ API."""

    llm_model: str = Field(..., min_length=1)
    llm_base_url: str = Field(default="https://backend.sovereigneg.com/v1")
    llm_temp: float = Field(default=0.0, ge=0.0, le=2.0)
    llm_max_tokens: int = Field(default=4096, ge=1)
    groq_key: str = Field(default="")
    gemini_key: str = Field(default="")
    tavily_key: str = Field(default="")
    firecrawl_key: str = Field(default="")
    opik_key: str = Field(default="")
    opik_project: str = Field(default="crew_project")

    @field_validator("llm_model", mode="before")
    @classmethod
    def _validate_model(cls, v: Any) -> str:
        text = (str(v) if v is not None else "").strip()
        if not text:
            raise ValueError("Model name cannot be empty.")
        return text

    def to_env_updates(self) -> dict[str, str]:
        return {
            "LLM_MODEL_NAME": self.llm_model,
            # فاضي = مقصود (للـ providers الرسمية زي gemini/ و openai/). مبنرجعوش للـ default هنا.
            "LLM_BASE_URL": (self.llm_base_url or "").strip(),
            "LLM_TEMPERATURE": str(self.llm_temp),
            "LLM_MAX_TOKENS": str(self.llm_max_tokens),
            "GROQ_API_KEY": (self.groq_key or "").strip(),
            "GEMINI_API_KEY": (self.gemini_key or "").strip(),
            "TAVILY_API_KEY": (self.tavily_key or "").strip(),
            "FIRECRAWL_API_KEY": (self.firecrawl_key or "").strip(),
            "OPIK_API_KEY": (self.opik_key or "").strip(),
            "OPIK_PROJECT_NAME": (self.opik_project or "crew_project").strip(),
        }

    

class RunTriggerResponse(BaseModel):
    """شكل الرد لما API خارجي يبدأ تشغيل الـ Crew."""
    status: str
    run_id: str
    message: str


def format_validation_error(err: ValidationError) -> str:
    """يطلع أول رسالة خطأ واضحة لعرضها في الواجهة."""
    first = err.errors()[0]
    msg = first.get("msg", "Invalid input")
    return msg.replace("Value error, ", "")