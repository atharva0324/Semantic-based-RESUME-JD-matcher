# Resume JD Matcher

An intelligent resume-job description matching system that combines **semantic similarity** and **NER-based skill extraction** to evaluate how well a candidate's resume matches a job description.

## What it does
1. Extracts technical skills and knowledge entities from both the JD and resume using a fine-tuned BERT NER model
2. Computes semantic similarity between extracted skill sets using Sentence Transformers
3. Computes exact keyword match score between extracted skills
4. Returns a weighted final score (80% semantic + 20% exact match)
5. Shows matched and missing skills clearly

## How it evolved
**v1 (baseline):**
- Used raw cosine similarity between full JD and resume text embeddings
- Single match percentage output
- No skill-level insight

**v2 (current):**
- Fine-tuned BERT on SkillSpan dataset for Named Entity Recognition
- Extracts knowledge entities (Python, Docker, AWS) from both JD and resume
- Semantic similarity computed on extracted skills only — not full text
- Combined scoring: semantic + exact keyword match
- Shows matched and missing skills to help candidates tailor their resume

## Tech Stack
- **NER Model**: BERT fine-tuned on SkillSpan dataset (`jjzha/skillspan`)
- **Embeddings**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Experiment Tracking**: MLflow

## Project Structure
resume-jd-matcher/

├── matcher.py              # Core matching logic

├── extractor.py            # NER skill extraction

├── app.py                  # FastAPI backend

├── frontend.py             # Streamlit UI

├── skill-extractor-model/  # Fine-tuned BERT NER model

└── requirements.txt
## How to run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the API
```bash
uvicorn app:app --reload
```

### 3. Start the UI
```bash
streamlit run frontend.py
```

## API Usage
```bash
curl -X POST "http://127.0.0.1:8000/match" \
-H "Content-Type: application/json" \
-d '{"jd": "your job description", "resume": "your resume text"}'
```

## Sample Response
```json
{
    "final_score": 72.5,
    "semantic_score": 81.3,
    "exact_match_score": 41.6,
    "matched_skills": ["python", "docker", "fastapi", "mlflow"],
    "missing_skills": ["kubernetes", "spark"],
    "inference_time_seconds": 0.54
}
```

## MLflow Tracking
Every match request is logged with scores and extracted skills.
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

## Model Details
- **Base model**: `bert-base-uncased`
- **Dataset**: SkillSpan (`jjzha/skillspan`) — 4800 training sentences from real job postings
- **Labels**: `B-SKILL`, `I-SKILL`, `B-KNOWLEDGE`, `I-KNOWLEDGE`, `O`
- **F1 Score**: 0.497 on validation set
- **Training**: 3 epochs, lr=2e-5, batch size=16 on Google Colab T4 GPU

## Why this approach?
Fine-tuned classifiers on full JD+resume text suffer from token length limitations and noise. By extracting skills first and then comparing semantically, we get a more focused and accurate match signal.