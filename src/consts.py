import os
LLM_SCORE_LIST="llm_responses"
PASS_SCORE=int(os.getenv("LLM_PASS_SCORE_THRESHOLD", 0.85))
FAIL_SCORE=int(os.getenv("LLM_FAIL_SCORE_THRESHOLD", 0.70))