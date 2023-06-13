"""
How to serialize LLM classes
https://python.langchain.com/en/latest/modules/models/llms/examples/llm_serialization.html
"""
from langchain.llms import OpenAI
from langchain.llms.loading import load_llm
from app.init import init_llm

init_llm(2)

llm = load_llm("llm.json")

print(llm('translate "大王八" to English'))

# save, only support json or yaml file
llm.save('llm.yaml')
