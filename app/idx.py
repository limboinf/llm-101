from abc import ABC, abstractmethod
import os
import pickle

from langchain.vectorstores import Chroma
from utils import get_project_root
from pathlib import Path


class AbstractIndexStorage(ABC):
    def __init__(self, save_folder):
        self._save_folder = save_folder

    @abstractmethod
    def save(self, *args, **kwargs):
        pass

    @abstractmethod
    def load(self, *args, **kwargs):
        pass


class ChromaIndexStorage(AbstractIndexStorage):

    def __init__(self, save_folder: str):
        super().__init__(save_folder)

    def save(self, db: Chroma):
        if not os.path.exists(self._save_folder):
            os.makedirs(self._save_folder)

        if db is None:
            return

        db.__setattr__('_persist_directory', self._save_folder)
        db.persist()
        return db

    def load(self, embedding):
        if not os.path.exists(self._save_folder):
            raise ValueError("未找到持久化文件")

        return Chroma(persist_directory=self._save_folder, embedding_function=embedding)


class FAISSIndexStorage(AbstractIndexStorage):
    def __init__(self, save_folder):
        super().__init__(save_folder)

    def save(self, vector_store, db_name: str):
        if not os.path.exists(self._save_folder):
            os.makedirs(self._save_folder)

        if db_name is None:
            return

        db_path = get_project_root() + f'/db/{db_name}_vector_store.pkl'
        with open(db_path, "wb") as f:
            pickle.dump(vector_store, f, pickle.HIGHEST_PROTOCOL)

    def load(self, db_name):
        db_path = get_project_root() + f'/db/{db_name}_vector_store.pkl'
        if not Path(db_path).exists():
            raise ValueError(f"{db_path} 不存在，请先 ingest")

        with open(db_path, 'rb') as f:
            vector_store = pickle.load(f)
        return vector_store