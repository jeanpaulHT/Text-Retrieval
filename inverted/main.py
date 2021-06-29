from index import MergeableIndex
from preprocessor import Preprocessor, make_ascii_compliant
from os import listdir
from os.path import isfile, join

import pickle

def main():
    mypath = "../texts/data_elecciones"
    json_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    text_dir = "../texts/data_elecciones"
    out_dir = "../texts/preprocessing"
    stop_list = "../texts/stoplist.txt"
    
    index_tmp_dir = "../texts/index"
    index_file = "../texts/index.txt"

    preprocessor = Preprocessor(text_dir, out_dir, stop_list)
    preprocessor.preprocess(["tweets_2018-09-29.json"])
    
    # # out_files = preprocessor.preprocess(json_files)

    # # remove later
    # out_names = [f for f in listdir(out_dir) if isfile(join(out_dir, f))]
    # print(out_names)
    # for out_name in out_names:
    #     out_file = join(out_dir, out_name)
    #     index = MergeableIndex(
    #         index_file=join(index_tmp_dir, out_name) + '.dat', 
    #         input_file=out_file, 
    #         build=True
    #     )
    #     print(len(index))
    
    # for a in n_index.items():
    #     print(a)



if __name__ == "__main__":
    main()