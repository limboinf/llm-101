"""
LangChain 的 llm_cache 是一个缓存，可用于存储和检索大型语言模型（LLM）的结果。这可以通过减少需要调用的次数来提高 LLM 的性能.
https://python.langchain.com/en/latest/modules/models/llms/examples/llm_caching.html
"""
import langchain

from app.init import init_llm
from langchain.llms import OpenAI
from gptcache import Cache
from gptcache.manager.factory import manager_factory
from gptcache.processor.pre import get_prompt
from gptcache.adapter.api import init_similar_cache

import hashlib
from langchain.cache import InMemoryCache, RedisCache, RedisSemanticCache, GPTCache
from redis import Redis
from langchain.embeddings import OpenAIEmbeddings
import time

init_llm(2)
#
# s = time.time()
# llm = OpenAI(model_name='text-davinci-002', n=2, best_of=2)
# print(llm('tell me a joke'))
# e = time.time()
# cost = e-s
# print(f'cost: {cost}')

# langchain.llm_cache = RedisCache(redis_=Redis())

# RedisSemanticCache
# 使用 Redis 缓存提示和响应，并根据语义相似性评估命中。
# 需要提前安装RediSearch https://docs.redis.com/latest/modules/redisearch/
# langchain.llm_cache = RedisSemanticCache(redis_url='redis://localhost:6379', embedding=OpenAIEmbeddings())

# 使用GPTCache 进行精确匹配缓存或基于语义相似性缓存结果
# https://github.com/zilliztech/GPTCache
def get_hashed_name(name):
    return hashlib.sha256(name.encode()).hexdigest()

def init_gptcache(cache_obj: Cache, llm: str):
    hashed_llm = get_hashed_name(llm)
    # 精准匹配
    # cache_obj.init(
    #     pre_embedding_func=get_prompt,
    #     data_manager=manager_factory(manager="map", data_dir=f"map_cache_{hashed_llm}"),
    # )
    # 相似度匹配
    init_similar_cache(cache_obj=cache_obj, data_dir=f"similar_cache_{hashed_llm}")


langchain.llm_cache = GPTCache(init_gptcache)

s = time.time()
llm = OpenAI(model_name='text-davinci-002', n=2, best_of=2)
print(llm('tell me a joke'))
e = time.time()
cost = e-s
print(f'cost: {cost}')


s = time.time()
print(llm('tell me a joke'))        # 精准匹配
print(llm('tell me one joke'))      # 相似度匹配
e = time.time()
cost = e-s
print(f'cost: {cost}')
