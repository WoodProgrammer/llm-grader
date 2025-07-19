from typing import List
from pydantic import BaseModel

class LLMResponse(BaseModel):
    question: str
    answer: str

class GoldenData(BaseModel):
    id: str
    question: str
    answer: str

class GoldenDataList(BaseModel):
    data: List[GoldenData]

