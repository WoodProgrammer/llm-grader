import os
LLM_SCORE_LIST="llm_responses"
PASS_SCORE=float(os.getenv("LLM_PASS_SCORE_THRESHOLD", 0.85))
FAIL_SCORE=float(os.getenv("LLM_FAIL_SCORE_THRESHOLD", 0.70))
N_RESULTS=int(os.getenv("N_RESULTS", 1))