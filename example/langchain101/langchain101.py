from app.init import init_llm

# import the LLM wrapper
# llms/__init__.py Wrappers on top of large language models APIs.
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from langchain.prompts.chat import (
    ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
)

# prompt management
from langchain.prompts import PromptTemplate

# 最核心的链类型是 LLMChain，它由 PromptTemplate 和 LLM 组成
from langchain.chains import LLMChain

# short-term memory vs long-term memory
from langchain import ConversationChain


init_llm()

# llm = OpenAI(temperature=0.9, model_name="gpt-3.5-turbo")
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
# print(llm("What would be a good company name for a company that makes colorful stones?"))

# prompt = PromptTemplate(
#     input_variables = ['product'],
#     template = 'What is a good name for a company that makes {product}'
# )
# # print(prompt.format(product='colorful stones'))
#
# chain = LLMChain(llm=llm, prompt=prompt)
# print(chain.run('colorful stones'))

# 默认 ConversationChain 有一种简单类型的内存，可以记住所有以前的输入/输出并将它们添加到传递的上下文中。设置 verbose=True 以便看到提示
# conversation = ConversationChain(llm=llm, verbose=True)
# print(conversation.predict(input='Say one!'))
# print(conversation.predict(input='Say two!'))
# print(conversation.predict(input='Say all above numbers!'))

# print(llm([HumanMessage(content='Translate this sentence into Chinese: I love you!')]))
# batch_messages = [
#     [
#         SystemMessage(content = 'You are a helpful assistant that translates English to Chinese.'),
#         HumanMessage(content = 'I love pig')
#     ],
#     [
#         SystemMessage(content='You are a helpful assistant that translates English to French.'),
#         HumanMessage(content='I love pig')
#     ],
# ]
# print(llm.generate(batch_messages))

template = "You are a helpful assistant that translates {input_language} to {output_language}."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)

human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
#
# output = llm(
#     chat_prompt.format_prompt(input_language='English', output_language='Chinese', text='I love you!').to_messages()
# )
# print(output)

# chain = LLMChain(llm=llm, prompt=chat_prompt)
# output = chain.run(input_language='English', output_language='Chinese', text='I love you!')
# print(output)

# from langchain.memory import ConversationBufferMemory
# prompt = ChatPromptTemplate.from_messages([
#     SystemMessagePromptTemplate.from_template("""
#         The following is a friendly conversation between a human and an AI.
#         The AI is talkative and provides lots of specific details from its context.
#         If the AI does not know the answer to a question, it truthfully says it does not know.
#     """),
#     MessagesPlaceholder(variable_name="history"),
#     HumanMessagePromptTemplate.from_template("{input}")
# ])
#
# memory = ConversationBufferMemory(return_messages=True)
# conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
# print(conversation.predict(input="What is your name?"))
# print(conversation.predict(input="I love programming."))
# print(conversation.predict(input="Tell me what we talk about."))

print(llm.get_num_tokens('lingoace learning platform'))    # token size 5
print(llm.get_num_tokens('kid chinese!'))       # token size 3
