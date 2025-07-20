import json
from fastapi import FastAPI, Response, HTTPException, status
from fastapi.responses import JSONResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from src.embed import Embedder
from src.consts import LLM_SCORE_LIST
from src.base_models import LLMResponse, GoldenDataList
from src.metrics import LLM_GRADE_SCORE

app = FastAPI()
embedding_service = Embedder()

@app.post("/api/v1/answers")
async def update_item(item: LLMResponse):
    try:
        embedding_service.redis_cli.rpush(
            LLM_SCORE_LIST,
            json.dumps({"id":item.id, "llm_output": item.llm_output})
        )

        return JSONResponse(
            content={"message": "LLM output successfully updated."},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while saving data to Redis: {str(e)}"
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

@app.get("/api/v1/metrics")
async def metrics():
    try:
        _llm_output_list = embedding_service.redis_cli.lrange(LLM_SCORE_LIST, 0, -1)
        grade_results = embedding_service._grade_llm_outputs(
            llm_outputs=[json.loads(item) for item in _llm_output_list])
        for result in grade_results:
            LLM_GRADE_SCORE.labels(
                qid=result["id"],
                similarity=result["similarity"], 
                grade=result["grade"]).set(result["hallucination_score"])

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Grading failed: {str(e)}"
        )
    
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run()