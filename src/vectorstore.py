from langchain_chroma import Chroma
from src.config import EMBEDDING_MODEL_ID
from src.bedrock_client import get_bedrock_runtime
from langchain_aws import BedrockEmbeddings

CHROMA_DIR = "chroma_db"

def get_embeddings():
    return BedrockEmbeddings(
        client = get_bedrock_runtime(),
        model_id = EMBEDDING_MODEL_ID
    )
def get_vectorstore():
    return Chroma(
        persist_directory = CHROMA_DIR,
        embedding_function = get_embeddings()
    )