from prometheus_client import Gauge

LLM_GRADE_SCORE = Gauge("llm_grade_score", "Grade score for llm similarity search",labelnames=["qid", "similarity", "grade"])
