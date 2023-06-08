from langchain.vectorstores import VectorStore
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

from app.ingest import Ingest
from app.init import init_llm
from typing import Optional

init_llm()

vector_store = Optional[VectorStore] = Ingest.load("xg")


def ask():
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())

    while True:
        query = input("> ")
        answer = qa.run(query)
        print(answer)


if __name__ == '__main__':
    ask()