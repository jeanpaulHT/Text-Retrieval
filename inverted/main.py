from index import MergeableIndex
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

    print(out_files)

    for out_file in out_files:
        out_name = out_file.lstrip(out_dir + '/')

        index = MergeableIndex(
            index_file=index_tmp_dir + '/' + out_name + '.dat', 
            input_file=out_file, 
            build=True
        )
        

        print(f"index:\n", index.post_entry('cmo'))



if __name__ == "__main__":
    main()