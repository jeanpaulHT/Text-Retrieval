from nltk.stem import SnowballStemmer
from typing import *
import os

class Index:
    _stemmer = SnowballStemmer('spanish')

    def __init__(self, index_dir: str, index_name: str, files: Iterable[str]):
        self.out_dir = index_dir
        self.out_name = index_name
        self.files = {(id, file) for id, file in enumerate(files)}
        self.normal = {}

        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        # self._build_index()

    def _build_index(self):
        for id, file in self.files:
            pass
