from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from matcher import match_resume

app = FastAPI(title="Resume JD Matcher")

class UserInput(BaseModel):
    jd: str
    resume: str

@app.get('/')
def home():
    return {"message": "Welcome to Resume JD Matcher"}

@app.post('/match')
def matching(data: UserInput):
    try:
        result = match_resume(data.jd, data.resume)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})