from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from extractor import extract_skills
import time
import mlflow

mlflow.set_tracking_uri("sqlite:////Users/atharvashinde/Desktop/resume-jd matcher/mlflow.db")
mlflow.set_experiment("resume-jd-matcher")

model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

def match_resume(jd: str, resume: str) -> dict:
    start_time = time.time()
    
   

    jd_extracted= extract_skills(jd)
    resume_extracted=extract_skills(resume)
    
    jd_all=set(jd_extracted ['knowledge'])
    resume_all=set(resume_extracted['knowledge'])

    jd_skills_text=" ".join(jd_all)
    resume_skills_text=" ".join(resume_all)

    jd_skills_encoded=model.encode(jd_skills_text)
    resume_skills_encoded=model.encode(resume_skills_text)

    score = cosine_similarity([jd_skills_encoded], [resume_skills_encoded])[0][0]
    semantic_score = round(float(score) * 100, 2)

    matched=jd_all.intersection(resume_all)
    missing=jd_all.difference(resume_all)

    exact_score=round(len(matched)/len(jd_all)*100,2) if jd_all else 0

    final_score=round(0.8 * semantic_score + 0.2 * exact_score,2)
    elapsed_time = round(time.time() - start_time, 3)
    
    with mlflow.start_run():
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("jd_length", len(jd))
        mlflow.log_param("resume_length", len(resume))
        mlflow.log_metric("match_score", final_score)
        mlflow.log_metric("inference_time", elapsed_time)
    
    return {
        "final_score": final_score,
        "semantic_score": round(semantic_score, 2),
        "exact_match_score": exact_score,
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "jd_skills": list(jd_all),
        "resume_skills": list(resume_all),
        "inference_time_seconds": elapsed_time
    }