from typing import *
import os
from collections import Counter
import pickle
import shutil
import os
import math

T = TypeVar('T')  

def calc_idf(N, df):
    return math.log10(N/df)

def calc_tf_idf(tf_td, idf):
    return math.log10(1 + tf_td) * idf
    
def merge_posts(a: Iterable, b: Iterable):
    i, j = iter(a), iter(b)
    val_i, val_j = next(i, None), next(j, None)
    if val_i is None and val_j is not None: yield val_j
    if val_j is None and val_i is not None: yield val_i

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

def merged_norms(a: Iterable, b: Iterable):
    iter_a, iter_b = iter(a), iter(b)
    
    cur_a: str = next(iter_a, None)
    cur_b: str =  next(iter_b, None)
    if cur_a is None and cur_b is not None: yield cur_b
    if cur_b is None and cur_a is not None: yield cur_a


    while cur_a is not None and cur_b is not None:
        cur_a = cur_a.rstrip('\n')
        cur_b = cur_b.rstrip('\n')
        (id_a, oc_a), (id_b, oc_b) = cur_a.split(' '), cur_b.split(' ')
        id_a, id_b = int(id_a), int(id_b)
        if id_a < id_b:
            yield cur_a + '\n'
            cur_a = next(iter_a, None)
        else:
            yield cur_b + '\n'
            cur_b = next(iter_b, None)

    yield from iter_a
    yield from iter_b

def merge_iters(a: Iterable, b: Iterable):
    i, j = iter(a), iter(b)
    val_i, val_j = next(i, None), next(j, None)

    if val_i is None and val_j is not None: yield val_j
    if val_j is None and val_i is not None: yield val_i

    while val_i is not None and val_j is not None:
        (str_i, post_i), (str_j, post_j) = val_i, val_j
        if str_i < str_j:
            yield val_i
            val_i = next(i, None)
        elif str_i > str_j:
            yield val_j
            val_j = next(j, None)
        else:
            new_post_list = list(merge_posts(post_i, post_j))
            yield str_i, new_post_list
            val_i, val_j = next(i, None), next(j, None)
    
    yield from i
    yield from j
    
def pairwise_iter(iterable: Iterable[T]) -> Iterable[Tuple[T, Optional[T]]]:
    iterator = iter(iterable)
    val = next(iterator, None)
    while val is not None:
        n = next(iterator, None)
        yield val, n
        val = next(iterator, None)


class MergeableIndex:
    ENTRY_SIZE = 128

    def __init__(self, 
            index_file: Optional[str]=None,
            input_file: Optional[str]=None, 
            build: bool=True, 
            no_action:bool=False
    ):
        self.index_file = index_file
        self.search_file = None if index_file is None else index_file + '.idx'
        self._size: int = 0

        if no_action is True:
            self._size = 0
        elif build is True:
            print(f'Building index for {index_file}')
            self._size = self._build_base_case_index(input_file)
        else:
            with open(self.search_file, 'rb') as f:
                f.seek(0, 2)
                self._size = (f.tell() // self.ENTRY_SIZE)

    def _build_base_case_index(self, in_file: str):
        tmp_index = {}
        with open(in_file, encoding="utf8") as f:
            for line in f:
                line = line.rstrip('\n')
                tweet_id_str, *words = line.split(' ')
                tweet_id = int(tweet_id_str)

                for word in filter(lambda x: x.rstrip('\n') != '', words):
                    counter: Counter = tmp_index.setdefault(word, Counter())
                    counter[tweet_id] += 1
        
        def make_list(l): 
            return sorted(l.items(), key=lambda x: x[0]) 

        def storable(w): 
            worst_case = (w, float('inf'), int(2**63))
            return len(pickle.dumps(worst_case)) <= self.ENTRY_SIZE

        index = { w: make_list(l) for w, l in tmp_index.items() if storable(w)}
        del tmp_index

        N = len(index)
        with open(self.index_file, 'wb') as f, open(self.search_file, 'wb') as s:
            pickler = pickle.Pickler(f)
            for string, posts in sorted(index.items()):
                idf = calc_idf(N, len(posts))

                tup = (string, idf, f.tell())
                dat = pickle.dumps(tup)
                diff = self.ENTRY_SIZE - len(dat)
                mod = dat + b'\0' * diff
                assert len(mod) == self.ENTRY_SIZE # assert fixed size

                s.write(mod)                
                pickler.dump((string, posts))

        del index
        return N
        
    def merge(self, other: 'MergeableIndex', name):
        tmp_f = name
        tmp_idx = name + '.idx'

        self_it = self.items()
        other_it = other.items()

        print(f"Merging {self.index_file} and {other.index_file} into {name}")

        with open(tmp_f, 'wb') as f, open(tmp_idx, 'wb') as idx:
            for string, posts in merge_iters(self_it, other_it):
                entry = (string, float(-1), f.tell())
                pos_str = pickle.dumps(entry)
                diff = self.ENTRY_SIZE - len(pos_str)
                idx.write(pos_str + b'\0' * diff)

                f_str = pickle.dumps((string, posts))
                f.write(f_str)
        
        return MergeableIndex(index_file=tmp_f, build=False)

    def dealloc_file(self):
        os.remove(self.index_file)
        os.remove(self.search_file)

    def keys(self):
        yield from (k for (k, v) in self.items())

    def values(self):
        yield from (v for (k, v) in self.items())

    def items(self):
        with open(self.index_file, 'rb') as f:
            unpickler = pickle.Unpickler(f)
            while True:
                try:
                    yield unpickler.load()
                except (EOFError, pickle.UnpicklingError):
                    break

    def static_items(self):
        with open(self.search_file, 'rb') as f:
            for i in range(len(self)):
                bytearr = f.read(self.ENTRY_SIZE)
                item = pickle.loads(bytearr)
                yield item

    def all_items(self):
        with open(self.index_file, 'rb') as f, open(self.search_file, 'rb') as s:
            unpickler = pickle.Unpickler(f)
            for i in range(len(self)):
                bytearr = s.read(self.ENTRY_SIZE)
                string, idf, _ = pickle.loads(bytearr)
                st, arr = unpickler.load()
                assert(st == string)

                yield string, idf, arr

    def post_entry(self, string): 
        with open(self.search_file, 'rb') as f:
            bin_search_index = self._make_bin_search(string, f)
            _, _, position = bin_search_index(0, len(self))
            if position is None:
                return None, None
            return self._postings_at(position)
    
    def static_entry(self, string):
        with open(self.search_file, 'rb') as f:
            bin_search_index = self._make_bin_search(string, f)
            return bin_search_index(0, len(self))

    def full_entry(self, string):
        with open(self.search_file, 'rb') as f:
            bin_search_index = self._make_bin_search(string, f)
            term, idf, position = bin_search_index(0, len(self))
            if position is None:
                return None, None, None

            _term, posts = self._postings_at(position)
            return term, idf, posts

    @staticmethod
    def _read_table_pos(f, p): 
        f.seek(p * MergeableIndex.ENTRY_SIZE)
        byte_str = f.read(MergeableIndex.ENTRY_SIZE)
        a = pickle.loads(byte_str)
        return a
                
    def _postings_at(self, position):
        with open(self.index_file, 'rb') as f:
            unpickler = pickle.Unpickler(f)
            f.seek(position)
            return unpickler.load()

    def _make_bin_search(self, string, file):
        def bin_search(begin, end):
            while begin < end:
                m = (begin + end) // 2
                comparable, idf, position = self._read_table_pos(file, m)
                if comparable == string: return (comparable, idf, position)
                elif comparable < string: begin = m + 1
                else: end = m
            
            return (None, None, None)

        return bin_search

    def _recalculate_idf(self):
        with open(self.search_file, 'r+b') as f:
            for i in range(len(self)):
                bytearr = f.read(self.ENTRY_SIZE)
                string, prev_idf, position = pickle.loads(bytearr)
                arr = self._postings_at(position)
                idf = calc_idf(len(self), len(arr))
                f.seek(-self.ENTRY_SIZE, 1)

                dat = pickle.dumps((string, idf, position))
                diff = self.ENTRY_SIZE - len(dat)
                mod = dat + b'\0' * diff
                assert len(mod) == self.ENTRY_SIZE # assert fixed size

                f.write(mod)

    def __len__(self):
        return self._size

    def __getitem__(self, val):
        if isinstance(val, str):
            return self.post_entry(val)
        elif isinstance(val, int):
            with open(self.search_file, 'rb') as f:
                _, position = self._read_table_pos(f, val)
                return self._postings_at(position)
        elif isinstance(val, slice):
            with open(self.search_file, 'rb') as f:
                start, stop, _ = val.indices(len(self))
                _, position = self._read_table_pos(f, start)
                return self._postings_at(position, stop - start)


class Index(MergeableIndex):
    NORM_ENTRY_SIZE = 32

    def __init__(self, index_file=None, files=None, norm_files=None, tmp_dir=None, build=True):
        no_action = True if build else False
        super().__init__(index_file=index_file, build=False, no_action=no_action)
        self.norm_file = f"{self.index_file}.norm"

        if build:
            self._build_index(files, tmp_dir)
            self._build_norm_file(norm_files, tmp_dir=tmp_dir)

    def _build_index(self, files, tmp_dir):
        indexes: List[MergeableIndex] = []
        
        filenames = [file.split('/')[-1] for file in files]
        for filename, file in zip(filenames, files):
            tmp = MergeableIndex(
                index_file=f"{tmp_dir}/{filename}.dat", 
                input_file=file,
                build=True
            )
            indexes.append(tmp)

        i = 0
        while len(indexes) > 1:
            next_indexes = []
            for first, second in pairwise_iter(indexes):
                if second is None: 
                    next_indexes.append(first)
                    break
                new_index = first.merge(second, f"{tmp_dir}/merge_{i}.dat")  
                i += 1
                next_indexes.append(new_index)    
                first.dealloc_file()
                second.dealloc_file()
                   
            indexes = next_indexes

        result: MergeableIndex = indexes[0]
        
        print("recalculating idf")
        result._recalculate_idf()

        print("moving index to final destination")
        shutil.move(result.index_file, self.index_file)
        shutil.move(result.search_file, self.search_file)
        self._size = len(result)
        
    def _build_norm_file(self, norm_files=None, tmp_dir=None):
        sorted_files = self._sort_norm_files(norm_files=norm_files)
        norms: List[str] = [file for file in sorted_files]

        i = 0
        print("Merging norm files")
        while len(norms) > 1:
            next_norms = []
            for first, second in pairwise_iter(norms):
                
                if second is None:
                    next_norms.append(first)
                    break
            
                new_norm_file = self.merge_norm_files(first, second, f"{tmp_dir}/norm_{i}.dat")
                print(f"Merged norm files {first} and {second} into {new_norm_file} ")
                next_norms.append(new_norm_file)
                i += 1
                # os.remove(first)
                # os.remove(second)
            norms = next_norms

        norm_src: str = norms[0]
        with open(norm_src, 'r') as src, open(self.norm_file, 'w+b') as dst:
            print(f"Binarizing temp file {norm_src} into {self.norm_file}")
            for id_str, norm_str in map(lambda x: x.rstrip('\n').split(' '), src.readlines()):
                id = int(id_str)
                norm = int(norm_str)
                dump = pickle.dumps((id, norm))
                assert(len(dump) <= self.NORM_ENTRY_SIZE)

                dump = dump.ljust(self.NORM_ENTRY_SIZE, b'\0')
                dst.write(dump)

                
            
    def get_norm(self, document):
        with open(self.norm_file, 'rb') as nf:
            nf.seek(0, 2)
            size = nf.tell() 
            size = size // self.NORM_ENTRY_SIZE
            nf.seek(0, 0)

            def read_norm_entry(pos):
                nf.seek(pos * self.NORM_ENTRY_SIZE)
                bytearr = nf.read(self.NORM_ENTRY_SIZE)
                load = pickle.loads(bytearr)
                return load
                
            def bin_search(begin, end):
                while begin < end:
                    m = (begin + end) // 2
                    doc_id, norm = read_norm_entry(m)
                    if doc_id == document: return norm
                    elif doc_id < document: begin = m + 1
                    else: end = m
            
                return 0

            return bin_search(0, size)

            
    
    @staticmethod
    def merge_norm_files(first, second, new_name):
        with open(new_name, 'w') as new, open(first, 'r') as f, open(second, 'r') as s:
            iterrows_a = f.readlines()
            iterrows_b = s.readlines()
            for line in merged_norms(iterrows_a, iterrows_b):
                new.write(line)
        return new_name

    @staticmethod
    def _sort_norm_files(norm_files=None):
        ret = []
        for file in norm_files:
            print(f"sorting base norm file {file}")
            lines = []
            with open(file, 'r') as f:
                lines = [line for line in f]

            sorted_name = f"{file}.sort"
            with open(sorted_name, 'w') as f:
                ret.append(sorted_name)
                for line in sorted(lines, key=lambda x: int(x.rstrip('\n').split(' ')[0])):
                    f.write(line)
        return ret

    
