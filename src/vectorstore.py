from functools import lru_cache
from langchain_chroma import Chroma
from langchain_aws import BedrockEmbeddings
from src.config import EMBEDDING_MODEL_ID, CHROMA_DIR
from src.bedrock_client import get_bedrock_runtime


@lru_cache(maxsize=1)
def get_embeddings():
    return BedrockEmbeddings(
        client=get_bedrock_runtime(),
        model_id=EMBEDDING_MODEL_ID,
    )


@lru_cache(maxsize=1)
def get_vectorstore():
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=get_embeddings(),
    )
