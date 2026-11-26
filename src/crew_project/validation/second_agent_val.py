# validation by pydantic
from pydantic import BaseModel,Field
from typing import List


class SingleSearchResult(BaseModel):
    title:str
    url:str = Field(...,title="the url page")
    content:str
    score:float
    search_query:str
    
class AllSearchResults(BaseModel):
    results:List[SingleSearchResult]

