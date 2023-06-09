import sys
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

from app.ingest import Ingest
from app.init import init_llm

init_llm()
embeddings = OpenAIEmbeddings()


def ask(db_path: str):
    vector_store = Ingest.load(db_path, embeddings)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())

    while True:
        query = input("> ")
        if query == 'exit':
            break

        answer = qa.run(query)
        print(answer)


if __name__ == '__main__':
    ask(sys.argv[1])