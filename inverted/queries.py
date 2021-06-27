from collections import deque
from index import Index


def query_and(list_1: list, list_2: list) -> list:
    res = []
    index1, index2 = 0, 0
    while index1 < len(list_1) and index2 < len(list_2):
        if list_1[index1] < list_2[index2]:
            index1 += 1
        elif list_2[index2] < list_1[index1]:
            index2 += 1
        else:
            res.append(list_1[index1])
            index1 += 1
            index2 += 1
    return res


def query_or(list_1: list, list_2: list) -> list:
    res = []
    i, j = 0, 0
    while True:
        if i == len(list_1):
            return res + list_2[j:]
        if j == len(list_2):
            return res + list_1[i:]
        if list_1[i] < list_2[j]:
            res.append(list_1[i])
            i += 1
        elif list_2[j] < list_1[i]:
            res.append(list_2[j])
            j += 1
        else:
            res.append(list_1[i])
            i += 1
            j += 1


def query_and_not(list_1: list, list_2: list) -> list:
    res = []
    i, j = 0, 0
    while i < len(list_1):
        if list_1[i] < list_2[j]:
            res.append(list_1[i])
            i += 1
        elif list_2[j] < list_1[i]:
            j += 1
        else:
            i += 1
            j += 1
    return res


class Query:

    def __init__(self, index: Index, query: str, use_cache: bool = True):
        self._tokens = self._tokenize_query(query)
        self._index = index
        self._use_cache = use_cache
        if use_cache:
            self.cache = dict()

    def eval(self):
        value = self._expression()
        Query._expect(self._current() is None, f"Expected end of query, got {self._current()}")
        return value

    def _expression(self):
        result = self._terminal()
        while self._current() == '+':
            self._advance()
            result = query_or(result, self._terminal())
        return result

    def _terminal(self):
        result = self._value()
        while self._current() in ('*', '-'):
            if self._current() == '*':
                self._advance()
                result = query_and(result, self._terminal())
            if self._current() == '-':
                self._advance()
                result = query_and_not(result, self._terminal())
        return result

    def _value(self):
        Query._expect(self._current() is not None, "Finished parsing without success")
        if self._current().isalpha():
            return self._load(self._consume())

        if self._current() == '(':
            self._advance()
            result = self._expression()
            Query._expect(self._consume() == ")", "Unmatched parenthesis on query")
            return result

        Query._fail(f"Expected a word or a nested query, got {self._current()}")

    def _load(self, word: str) -> list:
        if self._use_cache and word in self.cache:
            return self.cache[word]

        return_value = self._index.L(word)
        if self._use_cache:
            self.cache[word] = return_value

        return return_value

    @staticmethod
    def _expect(boolean_expr: bool, message: str) -> None:
        if not boolean_expr:
            Query._fail(message)

    @staticmethod
    def _fail(message: str) -> None:
        raise ValueError("Parser Error: ", message)

    def _current(self):
        return self._tokens[0] if len(self._tokens) > 0 else None

    def _consume(self):
        tmp = self._current()
        assert tmp is not None
        self._advance()
        return tmp

    def _advance(self):
        self._tokens.popleft()

    @staticmethod
    def _tokenize_query(query):
        processed = query.lower()
        processed = processed.replace(" and not ", " - ")
        processed = processed.replace(" and ", " * ")
        processed = processed.replace(" or ", " + ")
        processed = processed.replace("(", " ( ").replace(")", " ) ")
        return deque(processed.split())
