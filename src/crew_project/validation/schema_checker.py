from pydantic import BaseModel
from crew_project.core.configurations import groq_llm
from crew_project.validation.third_agent_val import ProductSpecification


def test_schema_compatibility(model_cls: type[BaseModel]):
    print(f"⏳ جاري اختبار: {model_cls.__name__} ...")
    try:
        response = groq_llm.call(
            messages=[
                {"role": "user", "content": "Generate one dummy example matching the required JSON schema."}
            ],
            response_model=model_cls,
        )
        print("✅ السيرفر قبل الـ Schema بنجاح! الرد التجريبي:")
        print(response)
    except Exception as e:
        print("❌ السيرفر رفض الـ Schema! سبب الرفض:")
        print(e)


if __name__ == "__main__":
    test_schema_compatibility(ProductSpecification)