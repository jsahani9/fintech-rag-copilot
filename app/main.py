import asyncio
from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.rag import answer_with_sources

app = FastAPI(
    title="FinTech RAG Copilot",
    description="OSFI Banking & Risk Intelligence API",
    version="0.2.0",
)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    k: int = 8


class AnswerResponse(BaseModel):
    answer: str
    sources: list[dict]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
async def ask_rag(req: QuestionRequest):
    """
    Main RAG endpoint.
    Runs the blocking Bedrock + retrieval pipeline in a worker thread.
    """
    answer_text, sources = await asyncio.to_thread(
        answer_with_sources,
        req.question,
        req.k,
    )
    return {"answer": answer_text, "sources": sources}
