"""
How to stream LLM and Chat Model responses
https://python.langchain.com/en/latest/modules/models/llms/examples/streaming_llm.html
"""
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage
from app.init import init_llm

init_llm(2)

# llm = OpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
# resp = llm("Write a poem about a happy boy, about 300 words.")

# 也可使用llm.generate 一次生成，但 streaming 目前不支持 token_usage
# resp = llm.generate(["Tell me a joke."])
# print(resp)

# use ChatOpenAI chat model
chat = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
resp = chat([HumanMessage(content="Write a poem about a happy girl, about 300 words.")])