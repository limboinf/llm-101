from langchain.embeddings import FakeEmbeddings, OpenAIEmbeddings
# from langchain.embeddings.openai import OpenAIEmbeddings

from app.init import init_llm

init_llm(2)

# embedding will gen 1536 float array size

embeddings = FakeEmbeddings(size=1024)
query_rs = embeddings.embed_query('foo')
doc_rs = embeddings.embed_documents(['foo'])

# OpenAIEmbeddings

eb2 = OpenAIEmbeddings()
txt = 'This is a test document'
query_rs = eb2.embed_query(txt)
doc_rs = eb2.embed_documents([txt])
print(doc_rs)
print(len(doc_rs[0]))


