import sys
from langchain.document_loaders import (
    TextLoader,
    UnstructuredWordDocumentLoader,
    DirectoryLoader,
    UnstructuredPDFLoader,
    UnstructuredHTMLLoader
)
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, TokenTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.vectorstores.weaviate import Weaviate
from langchain.vectorstores.chroma import Chroma
from langchain.document_loaders.directory import FILE_LOADER_TYPE
from langchain.docstore.document import Document
from langchain.vectorstores import VectorStore

from typing import Any, List, Optional, Type, Union
from dotenv import load_dotenv

from app.idx import ChromaIndexStorage
from app.consts import FileSuffix

load_dotenv()


class Ingest(object):
    def __init__(
            self,
            data_dir: str,
            file_type: str,
            db_path: str
    ):
        self.data_dir = data_dir
        self.file_type = FileSuffix.to_file_suffix(file_type)
        self.db_path = db_path

    def ingest_docs(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> Optional[VectorStore]:
        loader = DirectoryLoader(
            self.data_dir,
            glob=f'*.{self.file_type.value}',
            show_progress=True,
            loader_cls=_get_loader_cls(self.file_type)
        )
        raw: List[Document] = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=[" ", ",", "\n"])

        docs = text_splitter.split_documents(raw)
        embeddings = OpenAIEmbeddings()

        # vector_store = FAISS.from_documents(docs, embeddings)
        return ChromaIndexStorage(self.db_path).save(docs, embeddings)

    @staticmethod
    def load(db_path, embddings) -> VectorStore:
        return ChromaIndexStorage(db_path).load(embddings)


def _get_loader_cls(file_type: FileSuffix) -> FILE_LOADER_TYPE:
    if file_type == FileSuffix.TXT:
        loader_cls = TextLoader
    elif file_type == FileSuffix.DOC or file_type == FileSuffix.DOCS:
        loader_cls = UnstructuredWordDocumentLoader
    elif file_type == FileSuffix.PDF:
        loader_cls = UnstructuredPDFLoader
    elif file_type == FileSuffix.HTML:
        loader_cls = UnstructuredHTMLLoader
    else:
        raise NotImplementedError(f'file type: {file_type.name} has not implemented.')

    return loader_cls


if __name__ == '__main__':
    data_dir = sys.argv[1]
    file_suffix = sys.argv[2]
    db_path = sys.argv[3]

    chunk_size = 1000
    chunk_overlap = 200
    if len(sys.argv) == 5:
        chunk_size = int(sys.argv[4])
    if len(sys.argv) == 6:
        chunk_overlap = int(sys.argv[5])

    Ingest(data_dir, file_suffix, db_path).ingest_docs(chunk_size, chunk_overlap)