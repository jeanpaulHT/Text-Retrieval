from index import MergeableIndex, Index
from preprocessor import Preprocessor, make_ascii_compliant
from os import listdir
from os.path import isfile, join


import pickle

def main():
    mypath = "texts/data_elecciones"
    json_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    text_dir = "./texts/data_elecciones"
    out_dir = "./texts/preprocessing"
    stop_list = "./texts/stoplist.txt"
    
    index_tmp_dir = "./texts/index"
    index_file = "./texts/index.txt"

    preprocessor = Preprocessor(text_dir, out_dir, stop_list)    
    out_files = preprocessor._locate(json_files)

    index = Index(
        index_file=index_file, 
        files=out_files, 
        tmp_dir=index_tmp_dir, 
        build=False              # change this to actually build
    )

    print(len(index))
    for i in index.all_items():
        print(str(i)[:110])


if __name__ == "__main__":
    main()