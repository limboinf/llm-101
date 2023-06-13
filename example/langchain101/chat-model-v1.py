"""
ChatModel Basic
================
chat model is based around message rather than raw text.
docs: https://python.langchain.com/en/latest/modules/models/chat/getting_started.html
"""
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from app.init import init_llm
init_llm(2)

chat = ChatOpenAI(temperature=0)

# Message(Sys,Human) as chat input, and AIMessage as output.

resp: AIMessage = chat([
    SystemMessage(content="Please translate the following sentence into Chinese"),
    HumanMessage(content="python cookbook")
])
print(f"1:with message --> {resp}")


template = "You are a helpful assistant that translates {input_language} to {output_language}."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)

human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

resp: AIMessage = chat(chat_prompt.format_prompt(input_language="English", output_language="Chinese", text="I love you!").to_messages())
print(f"2:with template --> {resp}")


# 直接构建
prompt = PromptTemplate(
    template="You are a helpful assistant that translates {input_language} to {output_language}. the text is : {text}",
    input_variables=["input_language", "output_language", "text"],
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)
chat_prompt_v2 = ChatPromptTemplate.from_messages([system_message_prompt])

resp = chat(chat_prompt_v2.format_prompt(input_language="English", output_language="Chinese", text="I love you!").to_messages())
print(f"3:with template v2 --> {resp}")

### LLMChain
chain = LLMChain(llm=chat, prompt=chat_prompt)
rs_str = chain.run(input_language="English", output_language="Chinese", text="I love you!")
print(f"4:with LLMChain --> {rs_str}")

### with Streaming ChatOpenAI
chat = ChatOpenAI(temperature=0, streaming=True, callbacks=[StreamingStdOutCallbackHandler()],)
print(f"5:with Streaming --> ")
resp: AIMessage = chat(chat_prompt.format_messages(input_language="English", output_language="Chinese", text="I love you!"))