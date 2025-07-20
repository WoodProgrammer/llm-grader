from prometheus_client import Gauge, Counter

LLM_GRADE_SCORE = Gauge("llm_grade_score", "Grade score for llm similarity search",labelnames=["qid", "similarity", "grade"])
LLM_TOTAL_REQUEST_COUNT = Counter("llm_grade_count", "Number of grade request count")