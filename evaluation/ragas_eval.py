#!/usr/bin/env python3
"""
ragas_eval.py — RAGAS evaluation for FinTech RAG Copilot

Scores the existing RAG pipeline on 4 metrics using AWS Bedrock as the
judge LLM. No changes to FastAPI or Streamlit; completely standalone.

Usage:
    python evaluation/ragas_eval.py              # full 15-question run
    python evaluation/ragas_eval.py --questions 3  # quick 3-question smoke test
    python evaluation/ragas_eval.py --k 3          # retrieve 3 chunks per question
"""
import sys
import json
import time
import asyncio
import argparse
import warnings
from pathlib import Path
from datetime import datetime

# ── make src.* importable regardless of CWD ──────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

# Suppress the LangchainLLMWrapper deprecation noise — it still works fine
warnings.filterwarnings("ignore", message=".*LangchainLLMWrapper.*deprecated.*")

# ── ragas: use the legacy metric hierarchy that evaluate() actually accepts ───
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings.base import BaseRagasEmbedding
from ragas.metrics._faithfulness import Faithfulness
from ragas.metrics._answer_relevance import AnswerRelevancy
from ragas.metrics._context_precision import LLMContextPrecisionWithReference
from ragas.metrics._context_recall import LLMContextRecall
from ragas.dataset_schema import SingleTurnSample, EvaluationDataset
from ragas.run_config import RunConfig
from ragas import evaluate

from langchain_aws import BedrockEmbeddings, ChatBedrock

from src.config import LLM_MODEL_ID, EMBEDDING_MODEL_ID, AWS_REGION
from src.rag import format_context, ask_claude
from src.retriever import retrieve
from evaluation.golden_dataset import GOLDEN_DATASET

RESULTS_DIR = ROOT / "evaluation" / "results"


# ── RAGAS embeddings backed by the project's existing Bedrock setup ──────────

class BedrockRagasEmbedding(BaseRagasEmbedding):
    """
    Modern BaseRagasEmbedding using Bedrock Titan embeddings.
    AnswerRelevancy in ragas 0.4.x requires BaseRagasEmbedding (singular),
    not the legacy BaseRagasEmbeddings (plural) / LangchainEmbeddingsWrapper.
    """

    def __init__(self, model_id: str, region: str) -> None:
        super().__init__()
        self._lc = BedrockEmbeddings(model_id=model_id, region_name=region)

    def embed_text(self, text: str, **kwargs) -> list[float]:
        return self._lc.embed_query(text)

    # Legacy metrics expect the full LangChain embeddings interface
    def embed_query(self, text: str) -> list[float]:
        return self._lc.embed_query(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._lc.embed_documents(texts)

    async def aembed_text(self, text: str, **kwargs) -> list[float]:
        return await asyncio.get_running_loop().run_in_executor(
            None, lambda: self._lc.embed_query(text)
        )

    async def aembed_query(self, text: str) -> list[float]:
        return await self.aembed_text(text)

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        return await asyncio.get_running_loop().run_in_executor(
            None, lambda: self._lc.embed_documents(texts)
        )


# ── pipeline helpers ──────────────────────────────────────────────────────────

def run_pipeline(question: str, k: int) -> dict:
    """Run retrieve → format_context → ask_claude and return raw pieces."""
    docs = retrieve(question, k=k)
    return {
        "contexts": [d.page_content for d in docs],
        "answer": ask_claude(question, format_context(docs)),
    }


def build_dataset(items: list, k: int) -> EvaluationDataset:
    """Run the RAG pipeline for every golden item and assemble an EvaluationDataset."""
    samples = []
    total = len(items)
    for i, item in enumerate(items, start=1):
        print(f"  [{i:>2}/{total}] {item['question'][:72]}", flush=True)
        result = run_pipeline(item["question"], k=k)
        samples.append(
            SingleTurnSample(
                user_input=item["question"],
                retrieved_contexts=result["contexts"],
                response=result["answer"],
                reference=item["ground_truth"],
            )
        )
        if i < total:
            time.sleep(0.5)  # gentle on Bedrock rate limits between pipeline calls
    return EvaluationDataset(samples=samples)


# ── result parsing ────────────────────────────────────────────────────────────

# ragas uses these internal key names in the results DataFrame
_METRIC_LABELS = {
    "faithfulness":                         "Faithfulness",
    "answer_relevancy":                     "Answer Relevancy",
    "llm_context_precision_with_reference": "Context Precision",
    "context_recall":                       "Context Recall",
}


def extract_scores(result) -> dict[str, float]:
    """Return {metric_name: mean_score} from an EvaluationResult object."""
    df = result.to_pandas()
    numeric = df.select_dtypes(include="number")
    return {col: round(float(numeric[col].mean()), 4) for col in numeric.columns}


# ── reporting ─────────────────────────────────────────────────────────────────

def _rating(score: float) -> str:
    if score >= 0.85:
        return "excellent"
    if score >= 0.70:
        return "good"
    return "needs work"


def print_report(scores: dict, n_questions: int, elapsed: float) -> None:
    W = 64
    print(f"\n{'═' * W}")
    print(f"  RAGAS Evaluation Results — {datetime.now().strftime('%Y-%m-%d')}")
    print(f"  Questions: {n_questions}  |  Time: {elapsed:.0f}s")
    print(f"{'─' * W}")
    print(f"  {'Metric':<30}  {'Score':>8}  {'Rating':>10}")
    print(f"{'─' * W}")

    displayed = []
    for key, label in _METRIC_LABELS.items():
        if key in scores:
            v = scores[key]
            print(f"  {label:<30}  {v:>8.4f}  {_rating(v):>10}")
            displayed.append(v)

    if displayed:
        avg = sum(displayed) / len(displayed)
        print(f"{'─' * W}")
        print(f"  {'Overall Average':<30}  {avg:>8.4f}  {_rating(avg):>10}")
    print(f"{'═' * W}\n")


def save_report(scores: dict, dataset: EvaluationDataset, elapsed: float) -> Path:
    """Persist the full report (aggregate + per-question) to a timestamped JSON file."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = RESULTS_DIR / f"report_{ts}.json"

    report = {
        "generated_at": datetime.now().isoformat(),
        "model": LLM_MODEL_ID,
        "elapsed_seconds": round(elapsed, 1),
        "n_questions": len(dataset.samples),
        "scores": scores,
        "per_question": [
            {
                "question": s.user_input,
                "answer": s.response,
                "ground_truth": s.reference,
                "n_contexts": len(s.retrieved_contexts),
            }
            for s in dataset.samples
        ],
    }
    path.write_text(json.dumps(report, indent=2))
    return path


# ── entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="RAGAS evaluation — FinTech RAG Copilot")
    parser.add_argument(
        "--questions", type=int, default=len(GOLDEN_DATASET),
        help=f"Number of questions to run (default: all {len(GOLDEN_DATASET)})",
    )
    parser.add_argument(
        "--k", type=int, default=8,
        help="Retrieval top-k chunks per question (default: 8)",
    )
    args = parser.parse_args()
    items = GOLDEN_DATASET[: args.questions]

    print(f"\n{'═' * 64}")
    print(f"  FinTech RAG Copilot — RAGAS Evaluation")
    print(f"  Model    : {LLM_MODEL_ID}")
    print(f"  Questions: {len(items)}  |  Retrieval k: {args.k}")
    print(f"{'═' * 64}")

    # ── 1. Build judge LLM + embeddings (reuse project's Bedrock credentials) ─
    print("\n▸ Initializing Bedrock judge LLM and embeddings…")
    ragas_llm = LangchainLLMWrapper(
        ChatBedrock(
            model_id=LLM_MODEL_ID,
            region_name=AWS_REGION,
            model_kwargs={"temperature": 0.0, "max_tokens": 4096},
        )
    )
    ragas_embeddings = BedrockRagasEmbedding(model_id=EMBEDDING_MODEL_ID, region=AWS_REGION)

    metrics = [
        Faithfulness(llm=ragas_llm),
        AnswerRelevancy(llm=ragas_llm, embeddings=ragas_embeddings),
        LLMContextPrecisionWithReference(llm=ragas_llm),
        LLMContextRecall(llm=ragas_llm),
    ]

    # ── 2. Run RAG pipeline for every golden question ─────────────────────────
    print(f"\n▸ Running RAG pipeline on {len(items)} questions…")
    t0 = time.time()
    dataset = build_dataset(items, k=args.k)

    # ── 3. Score with RAGAS ───────────────────────────────────────────────────
    print("\n▸ Scoring with RAGAS (this may take several minutes)…")
    # max_workers=1 → sequential judge calls, avoids Bedrock ThrottlingException
    run_cfg = RunConfig(max_workers=1, timeout=120, max_retries=3)
    result = evaluate(dataset=dataset, metrics=metrics, run_config=run_cfg)
    elapsed = time.time() - t0

    # ── 4. Print + save report ────────────────────────────────────────────────
    scores = extract_scores(result)
    print_report(scores, len(items), elapsed)
    report_path = save_report(scores, dataset, elapsed)
    print(f"  Report saved → {report_path.relative_to(ROOT)}\n")


if __name__ == "__main__":
    main()
