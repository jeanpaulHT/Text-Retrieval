from nltk.stem import SnowballStemmer
from typing import *

import os
import json


class Preprocessor:
    skipped_symbols = {".", "?", "!", "¿", "<", ">", ",",
                       "º", " ", ":", ";", "«", "»", "(", 
                       ")", "\n", "\0", "@", "#", '\"', '-', '_', 
                       '+', '-', '*', '/', '|'}
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
            out_files.append(out_path)
            self._preprocess_file(in_path, out_path)
            print(f"preprocess for {file} done")
            n += 1
        print("preprocess completed")
        return out_files

    def _preprocess_text(self, line):
        result = ''
        for word in line:
            if word not in self.stop_list and not word.isnumeric():
                result += (self._stemmer.stem(word) + ' ')
        return result

    def _preprocess_file(self, in_path: str, out_path: str) -> None:
        with open(in_path, encoding="utf-8") as f_in, open(out_path, "w+", encoding="utf-8") as f_out:
            json_data = json.load(f_in)

            for tweet in json_data:
                # extracting  and parsing tweet text and erasing skipped symbols
                res = str(tweet['id']) + ' '
                if tweet.get('RT_text') is not None:
                    line = Preprocessor._parse_line(
                        tweet['RT_text'], self.skipped_symbols)
                    tweet['RT_text'] = self._preprocess_text(line)
                    res += tweet['RT_text']
                elif tweet.get('text') is not None:
                    line = Preprocessor._parse_line(
                        tweet['text'], self.skipped_symbols)
                    tweet['text'] = self._preprocess_text(line)
                    res += tweet['text']

                else:
                    exit(-1)
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
        word_list = line.split(" ")
        res = list()
        for word in word_list:
            new_word = "".join(c.lower() for c in word if c not in skipped)
            if len(new_word) != 0:
                res.append(new_word)
        return res
