from src.embed import Embedder
from src.base_models import LLMResponse, GoldenDataList
from fastapi import FastAPI

llm_outputs = [
    {"id": "q1", "llm_output": "Ankara"},
    {"id": "q2", "llm_output": "HTTPS http'nin güvenli halidir"}
]

app = FastAPI()
obj = Embedder()

@app.post("/api/v1/answers")
async def update_item(item: LLMResponse):
    results = {"answer": item.answer, "question": item.question}
    return results

@app.get("/api/v1/grade_answers")
async def grade_answers():
    results = obj._grade_llm_outputs(llm_outputs=llm_outputs)
    return results

@app.get("/api/v1/embed_structured_golden_answers")
async def embed_structured_golden_answers(item: GoldenDataList):
    results = obj._embed_data(golden_data=item["data"])
    return results

if __name__ == "__main__":
    app.run()