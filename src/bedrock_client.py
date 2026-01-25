import boto3
from src.config import AWS_REGION

def get_bedrock_runtime():
    return boto3.client("bedrock-runtime", region_name=AWS_REGION)