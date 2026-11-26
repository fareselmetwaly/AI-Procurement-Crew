# validation by pydantic
from pydantic import BaseModel,Field
from typing import List


class ProductSpecification(BaseModel):
    specification_name:str = Field(...,title="the product name")
    specification_value:str = Field(...,title="the value of product")


class SingleExtractedProduct(BaseModel):
    page_url:str = Field(...,title="the original page url")
    product_title:str = Field(...,title="the title of product")
    product_url:str = Field(...,title="the url of product")
    product_image_url:str = Field(...,title="the url of the product image")
    product_current_price:str = Field(...,title="the current price of product.")

    product_original_price: float | None = Field(title="The original price of the product before discount. Set to None if no discount", default=None)
    product_discount_percentage: float | None = Field(title="The discount percentage of the product. Set to None if no discount", default=None)


    product_specs: List[ProductSpecification] = Field(..., title="The specifications of the product (must contain between 1 and 5 key specs).")

    agent_recommendation_rank: int = Field(..., title="The rank of the product to be considered in the final procurement report. (out of 5, Higher is Better) in the recommendation list ordering from the best to the worst")
    agent_recommendation_notes: List[str]  = Field(..., title="A set of notes why would you recommend or not recommend this product to the company, compared to other products.")


class ExtractedProducts(BaseModel):
    products:List[SingleExtractedProduct]

