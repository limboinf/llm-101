"""
How to track token usage
https://python.langchain.com/en/latest/modules/models/llms/examples/token_usage_tracking.html
"""
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from app.init import init_llm

init_llm(2)

llm = OpenAI()
with get_openai_callback() as cb:
    result = llm('Tell me a joke')
    # cb is OpenAICallbackHandler object
    print(cb)
    print(result)