# 🏦 FinTech RAG Copilot
### Regulatory Intelligence Assistant for OSFI & Global FinTech Compliance

FinTech RAG Copilot is an end-to-end **Retrieval-Augmented Generation (RAG)** system that provides **grounded, citation-backed answers** to regulatory and compliance questions using official documents from **OSFI (Canada)** and internationally recognized cybersecurity and banking frameworks.

The system is designed to **prevent hallucinations**, respond only from retrieved source material, and clearly state when information is insufficient.

---

## 📊 Evaluation Results

Evaluated using [RAGAS](https://github.com/explodinggradients/ragas) on a 15-question golden dataset covering OSFI governance, cyber risk, third-party risk, NIST CSF, and BIS operational resilience guidelines. Judge LLM: AWS Bedrock (Claude Sonnet 4.5).

| Metric | Score | Rating |
|---|---|---|
| Faithfulness | **0.87** | ✅ Excellent |
| Answer Relevancy | **0.88** | ✅ Excellent |
| Context Precision | 0.26 | 🔧 In progress |
| Context Recall | 0.56 | 🔧 In progress |
| **Overall** | **0.64** | — |

**Faithfulness** measures whether the model's claims are grounded in the retrieved context (no hallucination). **Answer Relevancy** measures whether the response actually answers the question asked.

Context precision and recall are limited by the general-purpose Titan embedding model. Production improvements would include a cross-encoder reranker and hybrid BM25 + semantic search.

> Scores improved from an overall of **0.28 → 0.64** through iterative fixes: chunk size tuning (1000 → 1500 chars), MMR parameter tuning, a `format_context` truncation bug fix, and correcting golden dataset questions whose answers weren't present in the corpus.

---

## 🚀 Key Features

- 📄 PDF ingestion into a persistent vector database (Chroma)
- 🔍 Semantic search with MMR diversity (configurable top-k retrieval)
- 🤖 LLM via **AWS Bedrock (Claude Sonnet 4.5)**
- 🧠 Hallucination control — says "I don't know" when context is insufficient
- 📑 Inline citations `[1], [2]` referencing source documents and page numbers
- 🔗 Sources expander in UI showing retrieved document + page per answer
- ✅ Input validation (1–2000 chars) on the API
- 🌐 Streamlit frontend for interactive querying
- ⚡ FastAPI backend with async request handling
- 🐳 Fully Dockerized (API + UI via Docker Compose)
- 🧪 RAGAS evaluation pipeline with 15-question golden dataset

## 🧠 System Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        FinTech RAG Copilot System                        │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  Streamlit UI (Port 8501)                                          │  │
│  │  - User asks questions                                             │  │
│  │  - Configurable k (top-k chunks, default 8)                        │  │
│  │  - Displays grounded answers with citations + sources expander     │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                    │                                     │
│                                    ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  FastAPI Backend (Port 8000)                                       │  │
│  │  - POST /ask  →  { answer, sources[] }                             │  │
│  │  - Input validation (min 1, max 2000 chars)                        │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                    │                                     │
│                                    ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  RAG Pipeline                                                      │  │
│  │  ├─ Retriever (Chroma + MMR, k=8, fetch_k=48, lambda=0.7)         │  │
│  │  └─ LLM (AWS Bedrock / Claude Sonnet 4.5, max_tokens=1500)        │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                    │                                     │
│                                    ▼                                     │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  Vector Store (Chroma)                                             │  │
│  │  - 540 chunks, chunk_size=1500, overlap=300                        │  │
│  │  - Amazon Titan Embeddings                                         │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| LLM | AWS Bedrock — Claude Sonnet 4.5 |
| Embeddings | AWS Bedrock — Amazon Titan |
| Vector Store | ChromaDB |
| PDF Processing | PyPDF (LangChain loader) |
| Evaluation | RAGAS |
| Orchestration | LangChain |
| Deployment | Docker Compose |

---

## 📂 Project Structure

```
fintech_rag_copilot/
├── app/
│   └── main.py                  # FastAPI app, /ask endpoint, input validation
├── src/
│   ├── config.py                # Env vars (model IDs, AWS region, Chroma path)
│   ├── bedrock_client.py        # Boto3 Bedrock runtime client
│   ├── vectorstore.py           # Chroma + Titan embeddings (lru_cache)
│   ├── retriever.py             # MMR retrieval (k=8, fetch_k=48, lambda=0.7)
│   ├── rag.py                   # format_context, ask_claude, answer_with_sources
│   └── ingest.py                # PDF loader + chunker + Chroma ingestion
├── evaluation/
│   ├── golden_dataset.py        # 15 Q&A pairs across 7 regulatory documents
│   └── ragas_eval.py            # RAGAS scoring pipeline (Bedrock judge)
├── tests/
│   ├── test_api.py              # FastAPI endpoint tests
│   └── test_rag.py              # RAG pipeline unit tests
├── data/
│   └── pdfs/
│       ├── osfi/                # OSFI guidelines (6 documents)
│       └── international/       # BIS + NIST documents (4 documents)
├── streamlit_app.py             # Streamlit UI with sources expander
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.streamlit
└── requirements.txt
```

---

## 📄 Document Corpus (10 PDFs)

| Document | Coverage |
|---|---|
| OSFI Corporate Governance Guideline 2018 | Board duties, CRO, three lines of defence |
| OSFI Technology and Cyber Risk Management | Cyber risk framework, resilience |
| OSFI Technology and Cyber Incident Reporting | 72-hour reporting, incident fields |
| OSFI Third-Party Risk Management Guideline | Material arrangements, due diligence |
| OSFI Operational Risk Management and Resilience | BCP, impact tolerances |
| OSFI Foreign Entities Operating in Canada | Branch requirements |
| NIST Cybersecurity Framework 2.0 | 6 core functions (Govern, Identify, …) |
| BIS d431 — Fintech Implications for Banks | Supervisory challenges, suptech |
| BIS d516 — Principles for Operational Resilience | 7 operational resilience principles |
| BIS d146 — Cyber Resilience for FMIs | CPMI-IOSCO cyber resilience guidance |

---

## 🚀 Getting Started

### Prerequisites
- Docker + Docker Compose
- AWS account with Bedrock model access enabled

### 1. Configure environment

```env
# .env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_SESSION_TOKEN=your_session_token   # if using temporary credentials
EMBEDDING_MODEL_ID=amazon.titan-embed-text-v2:0
LLM_MODEL_ID=us.anthropic.claude-sonnet-4-5-20251001-v2:0
CHROMA_DIR=chroma_db
```

### 2. Ingest documents

```bash
python -m src.ingest
```

### 3. Run with Docker

```bash
docker compose up --build
```

### 4. Access

- **API docs**: http://localhost:8000/docs
- **Streamlit UI**: http://localhost:8501

---

## ⚙️ Configuration

| Variable | Description | Default |
|---|---|---|
| `AWS_REGION` | AWS region for Bedrock | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | AWS access key | Required |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Required |
| `EMBEDDING_MODEL_ID` | Titan embedding model | Required |
| `LLM_MODEL_ID` | Claude model ID | Required |
| `CHROMA_DIR` | ChromaDB persist path | `chroma_db` |

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

<<<<<<< HEAD
# Or use the Streamlit UI at http://localhost:8501
```

## 📸 Application Screenshots


### 1️⃣ Grounded Regulatory Answer (Structured + Cited)
Shows a multi-section, citation-backed response generated strictly from OSFI source documents.

<img width="1466" height="739" alt="structured_answer" src="https://github.com/user-attachments/assets/3b22338c-8c08-49f6-aa4c-81affa54eb76" />


---

### 2️⃣ Hallucination Control (No Unsupported Claims)
Demonstrates the system refusing to speculate when information is not present in the retrieved documents.

<img width="1488" height="694" alt="hallucination_control" src="https://github.com/user-attachments/assets/721a2a50-c2bf-436b-a4a5-89cbd1e5555a" />

---

### 3️⃣ Operational Compliance Guidance
Illustrates extraction of reporting timelines and notification requirements from regulatory guidance.

<img width="1492" height="766" alt="incident_reporting" src="https://github.com/user-attachments/assets/74737895-0e51-453b-9d96-5665eb8c0bc4" />


=======
12 tests covering API validation, RAG pipeline, context formatting, and source extraction.

## 📈 Running Evaluation

```bash
# Full 15-question run (~17 min, uses Bedrock as judge)
python evaluation/ragas_eval.py

# Quick 3-question smoke test
python evaluation/ragas_eval.py --questions 3

# Custom k
python evaluation/ragas_eval.py --k 10
```

Results are saved to `evaluation/results/report_<timestamp>.json`.

---

## 🔌 API Reference

### `POST /ask`

```json
// Request
{ "question": "What are OSFI's cyber risk expectations?", "k": 8 }

// Response
{
  "answer": "OSFI expects FRFIs to establish... [1][2]",
  "sources": [
    { "source": "Technology and Cyber Risk Management.pdf", "page": 4 },
    { "source": "OSFI Corporate Governance Guideline 2018.pdf", "page": 10 }
  ]
}
```

Validation: `question` must be 1–2000 characters.
>>>>>>> bab1c6d (Improve RAG quality, add evaluation pipeline, update README)
