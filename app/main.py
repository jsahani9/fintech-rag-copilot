import asyncio
from fastapi import FastAPI
from pydantic import BaseModel

from src.rag import answer

app = FastAPI(
    title="FinTech RAG Copilot",
    description="OSFI Banking & Risk Intelligence API",
    version="0.2.0",
)


class QuestionRequest(BaseModel):
    question: str
    k: int = 5


class AnswerResponse(BaseModel):
    answer: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
async def ask_rag(req: QuestionRequest):
    """
    Main RAG endpoint.
    Runs the blocking Bedrock + retrieval pipeline in a worker thread.
    """
    response_text = await asyncio.to_thread(
        answer,
        req.question,
        req.k
    )
    return {"answer": response_text}
