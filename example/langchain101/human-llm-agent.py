# use the human input LLM, 与 fake LLM (see falkllm.py) 类似，
# HumanInputLLM 可用于测试、调试及教育目的，模拟对LLM的调用，模拟人类在收到提示时的反应
# pip install wikipedia

from langchain.llms.human import HumanInputLLM
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

tools = load_tools(['wikipedia'])
llm = HumanInputLLM(prompt_func=lambda prompt: print(f"\n===PROMPT===\n{prompt}\n===END OF PROMPT===\n"))
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbost=True)
output = agent.run("有哪些海外中文教育水平考试？")
print(output)