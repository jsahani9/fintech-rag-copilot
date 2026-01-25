import json
from src.retriever import retrieve
from src.bedrock_client import get_bedrock_runtime
from src.config import LLM_MODEL_ID


def format_context(docs, max_chars: int = 12000) -> str:
    parts, used = [], 0
    for i, d in enumerate(docs, start=1):
        source = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", "unknown")
        text = d.page_content.strip()

        block = f"[{i}] SOURCE: {source} | PAGE: {page}\n{text}\n"
        if used + len(block) > max_chars:
            break
        parts.append(block)
        used += len(block)

    return "\n".join(parts)


def ask_claude(question: str, context: str) -> str:
    client = get_bedrock_runtime()

    system = (
        "You are a banking risk and compliance assistant. "
        "Answer ONLY using the provided CONTEXT. "
        "If the context is insufficient, say you don't know. "
        "Every factual claim must be cited like [1], [2]. "
        "You may summarize for clarity, but do not add new information."
    )

    user = f"""QUESTION:
{question}

CONTEXT:
{context}

INSTRUCTIONS:
- Use only the context above.
- If the answer is not explicitly supported, say:
  "I don't have enough information in the provided documents."
- Provide a concise answer with citations like [1], [2]."""

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 700,
        "temperature": 0.1,
        "system": system,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user}],
            }
        ],
    }

    resp = client.invoke_model(
        modelId=LLM_MODEL_ID,
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json",
    )

    data = json.loads(resp["body"].read())
    return data["content"][0]["text"]


def answer(question: str, k: int = 5) -> str:
    docs = retrieve(question, k=k)
    context = format_context(docs)
    return ask_claude(question, context)
