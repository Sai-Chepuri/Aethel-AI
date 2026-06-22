from pydantic import BaseModel
from typing import Optional


class ProductIdea(BaseModel):
    idea: str
    apiKey: Optional[str] = None

