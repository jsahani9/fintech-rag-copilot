import boto3
from functools import lru_cache
from src.config import AWS_REGION


@lru_cache(maxsize=1)
def get_bedrock_runtime():
    return boto3.client("bedrock-runtime", region_name=AWS_REGION)