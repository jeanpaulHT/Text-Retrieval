from nltk.stem import SnowballStemmer
from typing import *
import validators
import os
import json


import re



def make_ascii_compliant(text):
    return ''.join((c for c in text if len(c.encode()) == 1))


class Preprocessor:
    skipped_symbols = {"?", "!", "¿", "<", ">", '^'
                       "º", ":", ";", "«", "»", "(", 
                       ")", "{", "}", "[", "]", "\0", "@", "#", '=' 
                       '"', '-', '+', '*', '~'
                       '“', '”', '¡', '\'', '$', '%', '&', '"'}

    splitters = ['\r', '\n', ',', '-', '_', '|',  '/', '=', '.']

    _stemmer = SnowballStemmer('spanish')

    def __init__(self, in_dir: str, out_dir: str, stop_list_path: str):
        self.stop_list = self._load_stop_list(stop_list_path)
        self.in_dir = f"./{in_dir}/"
        self.out_dir = f"./{out_dir}/"
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

    def preprocess(self, files: Iterable[str]):
        out_files = []
        n = 0
        for file in files:
            print(f"{n}:preprocess for {file} starting......")
            in_path, out_path = self.in_dir + file, self.out_dir + file.split('.')[0]
            norm_path = f"{self.out_dir}../norm/" + str(file.split('.')[0])
            out_files.append(out_path)
            self._preprocess_file(in_path, out_path,norm_path)
            print(f"preprocess for {file} done")
            n += 1
        print("preprocess completed")
        return out_files

    def _locate(self, files: Iterable[str]):
        out_files = []
        for file in files:
            in_path, out_path = self.in_dir + file, self.out_dir + file.split('.')[0]
            out_files.append(out_path)
        return out_files

    def _preprocess_text(self, line):
        def gen():
            for word in line:
                word = make_ascii_compliant(word)
                if word not in self.stop_list and not word.isnumeric():
                    yield self._stemmer.stem(word)

        return ' '.join(gen())

    def _preprocess_file(self, in_path: str, out_path: str, norm_path : str) -> None:
        with open(in_path, encoding="utf-8") as f_in, open(out_path, "w+", encoding="utf-8") as f_out, open(norm_path , "w+", encoding="utf-8") as n_out:
            json_data = json.load(f_in)

            for lineno, tweet in enumerate(json_data, 1):

                # extracting  and parsing tweet text and erasing skipped symbols0
                res = str(tweet['id']) + ' '
                line = Preprocessor._parse_line(tweet['content'], self.skipped_symbols)
                line = self._preprocess_text(line)
                num = len(re.findall(r'\w+', line))

                n_out.write(f"{res}{num}" + '\n')

                res+= line


                f_out.write(res + '\n')

    @staticmethod
    def _load_stop_list(stop_list_path: str) -> set:
        stop_list = set()
        with open(stop_list_path, encoding="ISO-8859-1") as file:
            for line in file:
                stripped = line.strip(" \n")
                if len(stripped) == 0:
                    continue
                stop_list.add(stripped)
        return stop_list

    @staticmethod
    def _parse_line(line: str, skipped: Iterable) -> list:

        line = re.sub(r"http\S+", "", line)

        for splitter in Preprocessor.splitters:
            line = line.replace(splitter, ' ')

        word_list = line.split(' ')
        res = list()
        for word in word_list:

            if not word.isascii():
                word = make_ascii_compliant(word)

            if word.isalpha() or not (validators.url(word) or validators.email(word)):    
                new_word = "".join(c.lower() for c in word if c not in skipped)
                if len(new_word) != 0:
                    res.append(new_word)
        return res
