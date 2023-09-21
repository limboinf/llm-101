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
    print('Init OpenAI env')
    return openai


def _load_aiproxy():
    openai.proxy = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }
    openai.api_key = os.getenv("AIPROXY_API_KEY")
    openai.api_base = "https://api.aiproxy.io/v1"
    print('Init AIPROXY env')
    return openai


def init_llm(is_open_ai: bool = True):
    return _load_openai() if is_open_ai else _load_aiproxy()
