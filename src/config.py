from dotenv import load_dotenv
import os

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID")
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")

if not EMBEDDING_MODEL_ID:
    raise ValueError("EMBEDDING_MODEL_ID missing in .env")
if not LLM_MODEL_ID:
    raise ValueError("LLM_MODEL_ID missing in .env")
