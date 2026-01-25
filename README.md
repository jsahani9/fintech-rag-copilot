# 🏦 FinTech RAG Copilot  
### Regulatory Intelligence Assistant for OSFI & Global FinTech Compliance

FinTech RAG Copilot is an end-to-end **Retrieval-Augmented Generation (RAG)** system that provides **grounded, citation-backed answers** to regulatory and compliance questions using official documents from **OSFI (Canada)** and internationally recognized cybersecurity frameworks.

The system is designed to **prevent hallucinations**, respond only from retrieved source material, and clearly state when information is insufficient.

---

## 🚀 Key Features

- 📄 PDF ingestion into a persistent vector database (Chroma)
- 🔍 Semantic search with configurable top-k retrieval
- 🤖 Large Language Model via **AWS Bedrock (Claude Sonnet 4.5)**
- 🧠 Hallucination control (“Not enough information” when applicable)
- 📑 Inline citations `[1], [2]` referencing source documents
- 🌐 Streamlit frontend for interactive querying
- ⚡ FastAPI backend for scalable API access
- 🐳 Fully Dockerized (API + UI via Docker Compose)

## 🧠 System Architecture

The FinTech RAG Copilot is designed as a modular, production-style Retrieval-Augmented Generation (RAG) system with clear separation between UI, API, retrieval, and generation layers.

### High-Level Flow

1. **User Interaction (Streamlit UI)**
   - Users ask regulatory or compliance-related questions
   - Adjustable top-k retrieval for transparency and control
   - Displays grounded answers with inline citations

2. **API Layer (FastAPI)**
   - Exposes a `/ask` endpoint
   - Orchestrates retrieval and generation
   - Enforces response grounding and hallucination control

3. **Retrieval Layer (ChromaDB)**
   - Performs semantic similarity search over embedded documents
   - Uses top-k retrieval (and MMR for diversity where applicable)
   - Returns only relevant document chunks

4. **Generation Layer (AWS Bedrock)**
   - Uses Claude Sonnet 4.5 for answer generation
   - Strictly constrained to retrieved context
   - Returns “Not enough information” when sources are insufficient

5. **Data Layer**
   - Official OSFI guidance PDFs
   - Cybersecurity and compliance frameworks
   - Persisted vector embeddings using Amazon Titan

---

### Component Overview

| Component | Technology |
|--------|------------|
| Frontend | Streamlit |
| Backend API | FastAPI |
| LLM | AWS Bedrock (Claude Sonnet 4.5) |
| Embeddings | Amazon Titan |
| Vector Store | ChromaDB |
| Deployment | Docker + Docker Compose |


---

## 🛠️ Tech Stack

### Core Components
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **LLM**: AWS Bedrock (Claude Sonnet 4.5)
- **Vector Store**: Chroma
- **Embeddings**: Amazon Titan Embeddings
- **PDF Processing**: PyPDF

### Python Libraries
- `langchain`
- `langchain-community`
- `langchain-aws`
- `langchain-chroma`
- `chromadb`
- `pypdf`
- `streamlit`
- `fastapi`
- `uvicorn`
- `boto3`
- `python-dotenv`

---

## 📂 Project Structure

```
fintech-rag-copilot/
├── app/                    # FastAPI application
│   ├── main.py             # FastAPI app entry point
│   ├── config.py           # Configuration (model IDs, AWS regions)
│   ├── bedrock_client.py   # AWS Bedrock client
│   ├── retriever.py        # RAG retriever logic
│   └── vectorstore.py      # Chroma vector store management
├── data/                   # PDF documents (OSFI, frameworks)
├── chroma_db/              # Persistent vector store (generated)
├── .env                    # Environment variables
├── .env.example            # Environment template
├── .dockerignore           # Docker build ignore file
├── Dockerfile              # API Dockerfile
├── Dockerfile.streamlit    # Streamlit UI Dockerfile
├── docker-compose.yml      # Multi-container setup
├── requirements.txt        # Python dependencies
├── streamlit_app.py        # Streamlit frontend
└── README.md               # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Docker
- Docker Compose
- AWS Account with Bedrock access
- AWS Credentials configured

### 1. Configure AWS Credentials
Create a `.env` file in the project root:

```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_SESSION_TOKEN=your_session_token  # Optional
```

### 2. Build and Run

```bash
# Build and start containers
docker compose up --build
```

### 3. Access the Application
- **API**: http://localhost:8000
- **Streamlit UI**: http://localhost:8501

### 4. Stop the Application

```bash
docker compose down
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region for Bedrock | `us-east-1` |
| `AWS_ACCESS_KEY_ID` | AWS access key | Required |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Required |
| `CHROMA_DIR` | Chroma DB path | `/app/chroma_db` |
| `LLM_MODEL_ID` | Bedrock model ID | `anthropic.claude-sonnet-4-5-20250929-v1:0` |

### Docker Compose Options

| Command | Description |
|---------|-------------|
| `docker compose up --build` | Build and start both services |
| `docker compose up -d` | Start in detached mode |
| `docker compose down` | Stop services |
| `docker compose down -v` | Stop and remove volumes (clears DB) |

---

## 📂 Adding New Documents

To add new OSFI or framework documents:

1. Place PDF files in the `data/` directory:
   ```bash
   mkdir -p data
   cp /path/to/new_document.pdf data/
   ```

2. Rebuild and restart the API:
   ```bash
   docker compose up --build
   ```

   *Note: The vector store will be recreated with the new documents.*

---

## 🧪 Testing

### Example Questions

**OSFI-related:**
- "Summarize OSFI's expectations for cyber risk management."
- "What are the key requirements for cloud computing in Canadian financial institutions?"
- "Explain the principles of operational resilience for federally regulated entities."
- "What guidance does OSFI provide on third-party risk management?"

**Framework-related:**
- "What are the NIST CSF core functions?"
- "How does ISO 27001 address access control?"
- "Explain the key controls in the CIS Critical Security Controls."

### Testing with Docker

```bash
# Ask a question via API
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are OSFI's cyber risk expectations?", "k": 5}'

# Or use the Streamlit UI at http://localhost:8501
