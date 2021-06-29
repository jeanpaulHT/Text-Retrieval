from nltk.stem import SnowballStemmer
from typing import *
import os
from collections import Counter

class MergeableIndex:
    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file
        self._build_base_case_index()

    def _build_base_case_index(self):
        tmp_index = {} # Counter for each word

        with open(self.in_file, encoding="utf8") as f:
            for line in f:
                tweet_id, *words = line.split(' ')
                tweet_id = int(tweet_id)

                for word in words:
                    counter = tmp_index.setdefault(word, Counter())
                    counter[tweet_id] += 1
        
        for item in tmp_index.items():
            print(item)
        
        def make_item(l): return (len(l), sorted(l.items(), key=lambda x: x[1]))
        transform = { word: make_item(l) for word, l in tmp_index.items() }
        
        for a, b in transform.items():
            print(a, b)
        # transform = {
        #     word: (len(lst), sorted(lst, key=lambda x: len(x))) 
        #     for word, lst in tmp_index.items()
        # }
        # print(transform)

            


# class Index:
#     _stemmer = SnowballStemmer('spanish')

#     def __init__(self, index_dir: str, index_name: str, files: Iterable[str]):
#         self.out_dir = index_dir
#         self.out_name = index_name
#         self.files = {(id, file) for id, file in enumerate(files)}
#         self.normal = {}

#         if not os.path.exists(self.out_dir):
#             os.makedirs(self.out_dir)

#     def 