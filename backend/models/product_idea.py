from pydantic import BaseModel


class ProductIdea(BaseModel):
    idea: str
