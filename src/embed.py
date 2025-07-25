import chromadb
from chromadb.utils import embedding_functions
from src.consts import PASS_SCORE, FAIL_SCORE
import os
import redis
import logging

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

class Embedder(object):
    def __init__(self,embed_model="all-MiniLM-L6-v2"):
        client = chromadb.Client()
        redis_cli = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embed_model)
        self.collection = client.get_or_create_collection(name="golden_set", embedding_function=embedding_fn)
        self.redis_cli = redis_cli

    def _embed_data(self, golden_data=any):
        for item in golden_data:
            try:
                self.collection.add(
                    documents=[item.golden_answer],
                    metadatas=[{"prompt": item.prompt}],
                    ids=[item.id]
                )
                logging.info("Embedding in progress ...", item.id)
            
            except Exception as exp:
                logging.error("Error while embedding golden answers", exp)
                break
        
        logging.info("Embedding process has been completed properly", item.id)
    
    def _grade_llm_outputs(self,n_results, llm_outputs):
        results = []
        for item in llm_outputs:
            query = item["llm_output"]
            result = self.collection.query(query_texts=[query], n_results=n_results)
            score = result["distances"][0][0]
            similarity = 1 - score
            hallucination_score = round(score, 3)
            print("The similariy score is ", similarity)
            print("tHE pass Score is ", PASS_SCORE)
            print("tHE faİL Score is ", FAIL_SCORE)

            results.append({
                "id": item["id"],
                "llm_output": item["llm_output"],
                "most_similar_golden": result["documents"][0][0],
                "similarity": round(similarity, 3),
                "hallucination_score": hallucination_score,
                "grade": "PASS" if similarity > PASS_SCORE else "WARNING" if similarity > FAIL_SCORE else "FAIL"
            })
        
        return results