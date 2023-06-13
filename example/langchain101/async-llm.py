import time
import asyncio
from app.init import init_llm
from langchain.llms import OpenAI

init_llm()


def generate_serially():
    llm = OpenAI(temperature=0.9)
    for _ in range(3):
        resp = llm.generate(["Write a random nick name."])
        print(resp.generations[0][0].text)

async def async_generate(llm):
    resp = await llm.agenerate(["Write a random nick name."])
    print(resp.generations[0][0].text)

async def generate_concurrently():
    llm = OpenAI(temperature=0.9)
    tasks = [async_generate(llm) for _ in range(3)]
    await asyncio.gather(*tasks)

s = time.perf_counter()
asyncio.run(generate_concurrently())
elapsed = time.perf_counter() - s
print('\033[1m' + f"Concurrent executed in {elapsed:0.2f} seconds." + '\033[0m')

s = time.perf_counter()
generate_serially()
elapsed = time.perf_counter() - s
print('\033[1m' + f"Serially executed in {elapsed:0.2f} seconds." + '\033[0m')
