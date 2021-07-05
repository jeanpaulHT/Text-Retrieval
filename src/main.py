from src.index import Index
from src.preprocessor import Preprocessor
from src.queries import QueryEngine
from os import listdir
from os.path import isfile, join

mypath = "./texts/raw"
json_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

text_dir = "./texts/raw"
out_dir = "./texts/preprocessing"
stop_list = "./texts/stoplist.txt"
    
index_tmp_dir = "./texts/index"
index_file = "./texts/index.txt"

def get_out_and_norm_files(preprocessor: Preprocessor, json_files, rebuild):
    if rebuild:
        return preprocessor.preprocess(json_files)
    else:
        return preprocessor._locate(json_files)

def get_query_engine(preprocess=True, rebuild=True):
    preprocessor = Preprocessor(text_dir, out_dir, stop_list)
    
    out_files, norm_files = get_out_and_norm_files(preprocessor, json_files, preprocess)
    index = Index(index_file,out_files, norm_files, index_tmp_dir, rebuild)

    return QueryEngine(preprocessor, index)


def main():
    import cProfile
    import pstats

    engine = None
    with cProfile.Profile() as createEngine:
        engine = get_query_engine(preprocess=False, rebuild=False)
    
    stats = pstats.Stats(createEngine)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()

    query = "muere martin vizcarra"
    
    with cProfile.Profile() as searchInEngine:
        result = engine.search(query, 5)

    stats = pstats.Stats(searchInEngine)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()

    print(f"result={result}")

if __name__ == "__main__":
    main()