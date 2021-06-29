from nltk.stem import SnowballStemmer
from typing import *
import os
from collections import Counter
import pickle
import linecache
import sys
import itertools

def merge_posts(a, b):
    i, j = iter(a), iter(b)
    val_i, val_j = next(i, None), next(j, None)

    while val_i is not None and val_j is not None:
        (id_i, df_i), (id_j, df_j) = val_i, val_j
        if id_i < id_j:
            yield id_i, df_i
            val_i = next(i, None)
        elif id_i > id_j:
            yield id_j, df_j
            val_j = next(j, None)
        else:
            yield id_i, df_i + df_j
            val_i, val_j = next(i, None), next(j, None)

    yield from i
    yield from j


def merge_iters(a, b):
    i, j = iter(a), iter(b)
    val_i, val_j = next(i, None), next(j, None)

    while val_i is not None and val_j is not None:
        (str_i, post_i), (str_j, post_j) = val_i, val_j
        if str_i < str_j:
            yield str_i, post_i
            val_i = next(i, None)
        elif str_i > str_j:
            yield str_j, post_j
            val_j = next(j, None)
        else:
            new_post_list = list(merge_posts(post_i, post_j))
            yield str_i, new_post_list
            val_i, val_j = next(i, None), next(j, None)
    
    yield from i
    yield from j



class MergeableIndex:
    ENTRY_SIZE = 128

    def __init__(self, index_file=None, input_file=None, build=True):
        self.__index_file = index_file
        self.__search_file = None if index_file is None else index_file + '.idx'
        self.__size = 0

        if build is True:
            print(f'Building index for {index_file}')
            self.__size = self._build_base_case_index(input_file)
        else:
            with open(self.__search_file, 'rb') as f:
                f.seek(0, 2)
                self.__size = (f.tell() // self.ENTRY_SIZE)
        
    def __len__(self):
        return self.__size
        
    def __getitem__(self, val):
        if isinstance(val, str):
            return self._get_entry(val)
        elif isinstance(val, int):
            with open(self.__search_file, 'rb') as f:
                _, position = self._read_pos(f, val)
                return self._postings_at(position)
        elif isinstance(val, slice):
            with open(self.__search_file, 'rb') as f:
                start, stop, _ = val.indices(len(self))
                _, position = self._read_pos(f, start)
                return self._postings_at(position, stop - start)

    def keys(self):
        yield from (k for (k, v) in self.items())

    def values(self):
        yield from (v for (k, v) in self.items())

    def items(self):
        with open(self.__index_file, 'rb') as f:
            unpickler = pickle.Unpickler(f)
            while True:
                try:
                    yield unpickler.load()
                except (EOFError, pickle.UnpicklingError):
                    break

    def dealloc_file(self):
        os.remove(self.__index_file)
        os.remove(self.__search_file)
        

    def merge(self, other: 'MergeableIndex', name):
        tmp_f = name
        tmp_idx = name + '.idx'

        self_it = self.items()
        other_it = other.items()

        with open(tmp_f, 'wb') as f, open(tmp_idx, 'wb') as idx:
            for string, posts in merge_iters(self_it, other_it):
                entry = (string, f.tell())
                pos_str = pickle.dumps(entry)
                diff = self.ENTRY_SIZE - len(pos_str)
                idx.write(pos_str + b'\0' * diff)

                f_str = pickle.dumps((string, posts))
                f.write(f_str)
        
        return MergeableIndex(index_file=tmp_f, build=False)

        


        

        # push em all

    def _build_base_case_index(self, in_file):
        tmp_index = {}
        with open(in_file, encoding="utf8") as f:
            for lineno, line in enumerate(f):
                tweet_id, *words = line.split(' ')
                try:
                    tweet_id = int(tweet_id)
                except  ValueError:
                    print(f"Error on line: {lineno}, {line=}")
                    exit(-1)

                for word in filter(lambda x: x.rstrip('\n') != '', words):
                    counter = tmp_index.setdefault(word, Counter())
                    counter[tweet_id] += 1
        
        def make_list(l): return sorted(l.items(), key=lambda x: x[0]) 

        index = { word: make_list(l) for word, l in tmp_index.items() }
        line_index = {}

        del tmp_index
        with open(self.__index_file, mode='wb') as f:
            pickler = pickle.Pickler(f) 
            for a in sorted(index.items()):
                line_index[a[0]] = f.tell()
                pickler.dump(a)

        with open(self.__search_file, mode='wb') as f:
            for entry in line_index.items():  
                dat = pickle.dumps(entry)
                diff = self.ENTRY_SIZE - len(dat)
                f.write(dat + b'\0' * diff)
   
        size = len(index)
        del index
        return size

    @staticmethod
    def _read_pos(f, p): 
        f.seek(p * MergeableIndex.ENTRY_SIZE)
        byte_str = f.read(MergeableIndex.ENTRY_SIZE)
        return pickle.loads(byte_str)
                
    def _postings_at(self, position, number=1):
        with open(self.__index_file, 'rb') as f:
            unpickler = pickle.Unpickler(f)
            f.seek(position)
            ret = []
            for _ in range(number):
                ret.append(unpickler.load())
            return ret

    def _get_entry(self, string): 
        with open(self.__search_file, 'rb') as f:
            def bin_search_index(s, begin, end):
                if begin > end: return []
                m = (begin + end) // 2
                comparable, position = self._read_pos(f, m)
                if comparable == s: return self._postings_at(position)
                if comparable < s: return bin_search_index(s, m, end)
                return bin_search_index(s, begin, m)

            return bin_search_index(string, 0, len(self))


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