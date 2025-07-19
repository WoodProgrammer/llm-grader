from typing import List
from pydantic import BaseModel

class LLMResponse(BaseModel):
    id: str
    llm_output: str

class GoldenData(BaseModel):
    id: str
    prompt: str
    golden_answer: str

class GoldenDataList(BaseModel):
    data: List[GoldenData]

