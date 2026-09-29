from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import generate_learning_path

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    description="An AI-powered educational assistant for students.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class ExplainRequest(BaseModel):
    concept: str = Field(..., min_length=1, max_length=20000)
    level: str = "beginner"


class LearningPathRequest(BaseModel):
    goal: str = Field(..., min_length=1, max_length=20000)
    level: str = "beginner"
    timeline: str = "4 weeks"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(request: TextRequest):
    try:
        return {"answer": answer_question(request.text)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/explain")
async def explain(request: ExplainRequest):
    try:
        return {"explanation": explain_concept(request.concept, request.level)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/quiz")
async def quiz(request: TextRequest):
    try:
        return {"quiz": generate_quiz(request.text)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/summarize")
async def summarize(request: TextRequest):
    try:
        return {"summary": summarize_text(request.text)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/learn/recommendations")
async def learning_recommendations(request: LearningPathRequest):
    try:
        return {
            "learning_path": generate_learning_path(
                request.goal, request.level, request.timeline
            )
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
