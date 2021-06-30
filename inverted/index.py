from nltk.stem import SnowballStemmer
from typing import *
import os
from collections import Counter
import pickle
from cached_property import cached_property

import math

def _idf(N, df):
    return math.log10(N/df)

def _tf_idf(tf_td, idf):
    return math.log10(1 + tf_td) * idf



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

    def _build_base_case_index(self, in_file):
        tmp_index = {}
        with open(in_file, encoding="utf8") as f:
            for lineno, line in enumerate(f):
                line = line.rstrip('\n')
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
        def storable(w): 
            return len(pickle.dumps((w, float('inf'), int(2**63)))) <= self.ENTRY_SIZE

        index = { w: make_list(l) for w, l in tmp_index.items() if storable(w)}

        N = len(index)

        del tmp_index
        with open(self.__index_file, 'wb') as f, open(self.__search_file, 'wb') as s:
            pickler = pickle.Pickler(f)
            for string, posts in sorted(index.items()):
                idf = _idf(N, len(posts))

                tup = (string, idf, f.tell())
                dat = pickle.dumps(tup)
                diff = self.ENTRY_SIZE - len(dat)
                mod = dat + b'\0' * diff
                assert len(mod) == self.ENTRY_SIZE # assert fixed size

                s.write(mod)                
                pickler.dump((string, posts))





        # with open(self.__search_file, mode='wb') as f:
        #     for string, (position, df) in line_index.items():  
        #         idf = _idf(N, df)
        #         dat = pickle.dumps((string, idf, position))
        #         diff = self.ENTRY_SIZE - len(dat)
        #         f.write(dat + b'\0' * diff)
   
        del index
        return N
        
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

    def dealloc_file(self):
        os.remove(self.__index_file)
        os.remove(self.__search_file)

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

    def static_items(self):
        with open(self.__search_file, 'rb') as f:
            for i in range(len(self)):
                bytearr = f.read(self.ENTRY_SIZE)
                if len(bytearr) < self.ENTRY_SIZE:
                    print(f"{bytearr=}")
                item = pickle.loads(bytearr)
                yield item
    
        with open(self.__index_file, 'rb') as f, open(self.__search_file, 'rb') as s:
            unpickler = pickle.Unpickler(f)
            for i in range(len(self)):
                bytearr = s.read(self.ENTRY_SIZE)
                string, idf, _ = pickle.loads(bytearr)
                st, arr = unpickler.load()
                assert(st == string)

                yield string, idf, arr

    def post_entry(self, string): 
        with open(self.__search_file, 'rb') as f:
            bin_search_index = self._make_bin_search(string, f)
            _, _, position = bin_search_index(0, len(self))
            if position is None:
                return None, None
            return self._postings_at(position)
    
    def static_entry(self, string):
        with open(self.__search_file, 'rb') as f:
            bin_search_index = self._make_bin_search(string, f)
            return bin_search_index(0, len(self))

    def _make_bin_search(self, string, file):
        def bin_search(begin, end):
            if begin >= end: return (None, None, None)
            m = (begin + end) // 2
            comparable, idf, position = self._read_table_pos(file, m)
            if comparable == string: return (comparable, idf, position)
            if comparable < string: return bin_search(m + 1, end)
            return bin_search(begin, m)

        return bin_search

    def full_entry(self, string):
        with open(self.__search_file, 'rb') as f:
            bin_search_index = self._make_bin_search(string, f)
            term, idf, position = bin_search_index(0, len(self))
            if position is None:
                return None, None, None

            _term, posts = self._postings_at(position)
            assert(string == term == _term)
            return term, idf, posts

    @staticmethod
    def _read_table_pos(f, p): 
        f.seek(p * MergeableIndex.ENTRY_SIZE)
        byte_str = f.read(MergeableIndex.ENTRY_SIZE)
        a = pickle.loads(byte_str)
        return a
                
    def _postings_at(self, position, number=1):
        with open(self.__index_file, 'rb') as f:
            unpickler = pickle.Unpickler(f)
            f.seek(position)
            return unpickler.load()

    def __len__(self):
        return self.__size

    def __getitem__(self, val):
        if isinstance(val, str):
            return self.post_entry(val)
        elif isinstance(val, int):
            with open(self.__search_file, 'rb') as f:
                _, position = self._read_table_pos(f, val)
                return self._postings_at(position)
        elif isinstance(val, slice):
            with open(self.__search_file, 'rb') as f:
                start, stop, _ = val.indices(len(self))
                _, position = self._read_table_pos(f, start)
                return self._postings_at(position, stop - start)
