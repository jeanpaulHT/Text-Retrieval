from index import Index
from preprocessor import Preprocessor
from queries import QueryEngine
from os import listdir
from os.path import isfile, join

def main():
    mypath = "../texts/raw"
    json_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    text_dir = "../texts/raw"
    out_dir = "../texts/preprocessing"
    stop_list = "../texts/stoplist.txt"
    
    index_tmp_dir = "../texts/index"
    index_file = "../texts/index.txt"

    preprocessor = Preprocessor(text_dir, out_dir, stop_list)    
    out_files = preprocessor._locate(json_files)
    preprocessor.preprocess(["covid_data0.json"])

    # index = Index(
    #     index_file=index_file,
    #     files=out_files,
    #     tmp_dir=index_tmp_dir,
    #     build=False              # change this to actually build
    # )
    #
    # engine = QueryEngine(preprocessor, index, 5)
    # engine.search("muere martin vizcarra")


if __name__ == "__main__":
    main()