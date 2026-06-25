from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time
import mlflow

mlflow.set_tracking_uri("sqlite:////Users/atharvashinde/Desktop/resume-jd matcher/mlflow.db")
mlflow.set_experiment("resume-jd-matcher")

model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

def match_resume(jd: str, resume: str) -> dict:
    start_time = time.time()
    
    jd_encoded = model.encode(jd)
    resume_encoded = model.encode(resume)
    
    score = cosine_similarity([jd_encoded], [resume_encoded])[0][0]
    match_percentage = round(float(score) * 100, 2)
    elapsed_time = round(time.time() - start_time, 3)
    
    with mlflow.start_run():
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("jd_length", len(jd))
        mlflow.log_param("resume_length", len(resume))
        mlflow.log_metric("match_score", match_percentage)
        mlflow.log_metric("inference_time", elapsed_time)
    
    return {
        "match_percentage": match_percentage,
        "inference_time_seconds": elapsed_time,
        "model_used": model_name
    }