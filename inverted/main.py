from index import MergeableIndex
from preprocessor import Preprocessor
# from queries import Query
from os import listdir
from os.path import isfile, join


def main():
    mypath = "../texts/data_elecciones"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    text_dir = "../texts/data_elecciones"
    out_dir = "../texts/preprocessing"
    stop_list = "../texts/stoplist.txt"
    index_file = "../texts/index.txt"

    preprocessor = Preprocessor(text_dir, out_dir, stop_list)
    # out_files = preprocessor.preprocess(onlyfiles)

    index = MergeableIndex('../texts/preprocessing/tweets_2018-08-07', "../texts/index/tmp_batch_1")

    # index = Index(out_files)
    # index.dump(index_file)

    # query = Query(index, input("Ingrese una query: "))
    # print("result: ", query.eval())


if __name__ == "__main__":
    main()

    # term1 = _index.L("Bilbo")
    # term2 = _index.L("Anillo")
    # term3 = _index.L("Montaña")
    #
    # print(term1, term2, term3)
    #
    # print(query_and(term1, term2))
    # print(query_or(term1, term2))
    # print(query_and_not(term3, term1))
    # print(query_and_not(term1, term3))
    # print(query_and(term2, term3))
    # print(query_or(term1, term3))

    # query = Query(
    #   _index, "Fangorn or (Bilbo and not Montaña) or (Montaña and not Bilbo)")
