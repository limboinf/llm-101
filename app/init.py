import os
import openai
from dotenv import load_dotenv

load_dotenv()


def _load_openai():
    openai.proxy = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    openai.api_key = os.getenv("OPENAI_API_KEY")
    return openai


def _load_aiproxy():
    openai.proxy = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    openai.api_key = os.getenv("AIPROXY_API_KEY")
    openai.api_base = "https://api.aiproxy.io/v1"
    return openai


def init_llm(t: int = 0):
    if t == 0:
        return _load_openai()
    return _load_aiproxy()
