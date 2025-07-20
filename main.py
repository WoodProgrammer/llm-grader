from src.embed import Embedder
from src.base_models import LLMResponse, GoldenDataList
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

app = FastAPI()
embedding_service = Embedder()

_llm_output_list = []

@app.post("/api/v1/answers")
async def update_item(item: LLMResponse):
    _llm_output_list.append({
        "id": item.id,
        "llm_output": item.llm_output
    })
    return JSONResponse(
        content={"message": "LLM output successfully updated."},
        status_code=status.HTTP_200_OK
    )

@app.post("/api/v1/embed_structured_golden_answers")
async def embed_structured_golden_answers(item: GoldenDataList):
    try:
        embedding_service._embed_data(golden_data=item.data)
        return "OK"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Embedding failed: {str(e)}"
        )

@app.get("/api/v1/grade_answers")
async def grade_answers():
    try:    
        grade_results = embedding_service._grade_llm_outputs(llm_outputs=_llm_output_list)
        return grade_results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Grading failed: {str(e)}"
        )

if __name__ == "__main__":
    app.run()