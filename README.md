# Resume JD Matcher

A semantic resume-job description matching system using Sentence Transformers.

## What it does
Takes a job description and a resume, computes semantic similarity using sentence embeddings, and returns a match percentage.

## Tech Stack
- **Model**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Experiment Tracking**: MLflow

## Project Structure
resume-jd-matcher/

├── matcher.py      # Core matching logic

├── app.py          # FastAPI backend

├── frontend.py     # Streamlit UI

├── requirements.txt

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
-d '{"jd": "your job description", "resume": "your resume"}'
```

## MLflow Tracking
Every match request is logged to MLflow with match score, inference time, and model name.
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

## Why Sentence Transformers?
Traditional fine-tuned classifiers require large labeled datasets and significant compute. Sentence transformers provide strong semantic understanding out of the box, making them ideal for semantic similarity tasks like resume matching.