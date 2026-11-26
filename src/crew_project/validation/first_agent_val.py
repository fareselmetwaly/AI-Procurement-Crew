# validation by pydantic
from pydantic import BaseModel,Field
from typing import List
# الحد الأقصى هنا لازم يطابق le=20 في ProcurementRequest.no_keywords.
# قبل كده كان بيتقرا من latest_config.json وقت الـ import (قيمة قديمة من آخر run) فكان بيرفض الـ output لو زوّدت العدد.
MAX_QUERIES = 20


class SearchQueriesJSON(BaseModel):
    queries:List[str] = Field(...,title="Suggested search queries to be passed to the search engine",min_length=1, max_length=MAX_QUERIES)
