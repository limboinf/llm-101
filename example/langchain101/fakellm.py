# how and why to use the fake LLM
# docs: https://python.langchain.com/en/latest/modules/models/llms/examples/fake_llm.html
# class FakeListLLM(LLM) 一个自定义的LLM (see custom-llm.py)

from langchain.llms.fake import FakeListLLM
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

tools = load_tools(['python_repl'])

responses = [
    "(fake) ... Action: Python REPL\nAction Input: print(2 + 2)",
    "Final Answer: 4"
]
llm = FakeListLLM(responses=responses)

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
print(agent.run("whats 2+2"))