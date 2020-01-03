"""Project4
CPE202

Darya Darvish
"""

import math
import os
from hashtables import HashTableLinear, HashTableSepchain, HashTableQuadratic, import_stopwords


class SearchEngine:
    """class for SearchEngine
    Attributes:
        directory (str) : a directory name
        stopwords (HashMap) : a hash table containing stopwords
        doc_length (HashMap) : a hash table containing the total number of words in each
                                document
        term_freqs (HashMap) : a hash table of hash tables for each term. Each hash table
                                contains the frequency of the term in documents
                                (document names are the keys and the frequencies are the values)
        file_list : a list of files
    """
    def __init__(self, directory, stopwords):
        self.doc_length = HashTableLinear()  # Replace HashMap() with your hash table.
        self.term_freqs = HashTableLinear()
        self.stopwords = stopwords
        self.index_files(directory)

    def __repr__(self):
        return "doc_length: %s, term_freqs: %s, stopwords: %s"\
               % (self.doc_length, self.term_freqs, self.stopwords)

    def __eq__(self, other):
        return isinstance(other, SearchEngine) and self.doc_length == other.doc_length\
            and self.term_freqs == other.term_freqs

    def read_file(self, infile):
        """A helper function to read a file
        Args:
        infile (str) : the path to a file
        Returns:
        list : a list of str read from a file
        """
        file_list = []
        with open(infile, 'r') as i:
            for line in i.readlines():
                file_list.append(line)
        return file_list

    def parse_words(self, lines):
        """split strings into words
        Convert words to lower cases and remove new line chars.
        Exclude stopwords.
        Args:
        lines (list) : a list of strings
        Returns:
        list : a list of words
        """
        word_list = []
        for item in lines:
            split_arr = item.split(' ')
            for word in split_arr:
                if word != '\n':
                    word_list.append(word.lower())
        final_arr = []
        for item in word_list:
            item = item.replace("(", '')
            item = item.replace(")", '')
            item = item.replace(".", '')
            item = item.replace(",", '')
            final_arr.append(item.rstrip())
        final_arr = self.exclude_stopwords(final_arr)
        return final_arr

    def exclude_stopwords(self, terms):
        """exclude stopwords from the list of terms
        Args:
        terms (list) :
        Returns:
        list : a list of str with stopwords removed
        """
        new_terms = []
        for item in terms:
            if item in self.stopwords:
                continue
            else:
                new_terms.append(item)
        return new_terms

    def count_words(self, filename, words):
        """count words in a file and store the frequency of each
        word in the term_freqs hash table. The keys of the term_freqs hash table shall be
        words. The values of the term_freqs hash table shall be hash tables (term_freqs
        is a hash table of hash tables). The keys of the hash tables (inner hash table) stored
        in the term_freqs shall be file names. The values of the inner hash tables shall be
        the frequencies of words. For example, self.term_freqs[word][filename] += 1;
        Words should not contain stopwords.
        Also store the total count of words contained in the file in the doc_length hash table.
        Args:
        filename (str) : the file name
        words (list) : a list of words
        """
        for item in words:
            if self.term_freqs.contains(item):
                if self.term_freqs[item].contains(filename):
                    self.term_freqs[item][filename] += 1
                else:
                    self.term_freqs[item].put(filename, 1)
            else:
                ht = HashTableLinear()
                ht.put(filename, 1)
                self.term_freqs.put(item, ht)
            if self.doc_length.contains(filename):
                self.doc_length[filename] += 1
            else:
                self.doc_length.put(filename, 1)

    def index_files(self, directory):
        """index all text files in a given directory
        Args:
        directory (str) : the path of a directory
        """
        dir_list = os.listdir(directory)
        for item in dir_list:
            if os.path.isfile(os.path.join(directory, item)) is True:
                parts = os.path.splitext(item)
                if parts[1] == '.txt':
                    line_arr = self.read_file(os.path.join(directory, item))
                    words = self.parse_words(line_arr)
                    self.count_words(os.path.join(directory, item), words)

    def get_wf(self, tf):
        """computes the weighted frequency
        Args:
        tf (float) : term frequency
        Returns:
        float : the weighted frequency
        """

        if tf > 0:
            wf = 1 + math.log(tf)
        else:
            wf = 0
        return wf

    def get_scores(self, terms):
        """creates a list of scores for each file in corpus
        The score = weighted frequency / the total word count in the file.
        Compute this score for each term in a query and sum all the scores.
        Args:
        terms (list) : a list of str
        Returns:
        list : a list of tuples, each containing the filename and its relevancy score
        """
        scores = HashTableLinear()
        for item in terms:
            if item in self.term_freqs:
                temp = self.term_freqs[item]
                for thing in temp.hash_table:
                    if thing is not None:
                        if thing[0] in scores:
                            scores[thing[0]] += self.get_wf(thing[1])
                        else:
                            scores.put(thing[0], self.get_wf(thing[1]))
        for item in scores.hash_table:
            if item is None:
                continue
            else:
                scores[item[0]] /= self.doc_length[item[0]]
        return scores

    def rank(self, scores):
        """ranks files in the descending order of relevancy
        Args:
        scores(list) : a list of tuples: (filename, score)
        Returns:
        list : a list of tuples: (filename, score) sorted in descending order of relevancy
        """
        new_scores = list(filter(None, scores))
        sorted_scores = sorted(new_scores, key=lambda x: x[1], reverse=True)
        return sorted_scores

    def search(self, query):
        """ search for the query terms in files
        Args:
        query (str) : query input
        Returns:
        list : list of files in descending order or relevancy
        """
        scores = self.get_scores(query).hash_table
        new_scores = self.rank(scores)
        score_arr = []
        for item in new_scores:
            if item is not None:
                score_arr.append(item)
                print(item)
        return score_arr


def keys(hashtable):
    key_array = []
    for item in hashtable.hash_table:
        if item is not None:
            key_item = item[0]
            key_array.append(key_item)
    return key_array


def main():
    # execute unit tests
    directory = input("please enter a directory name\n")
    yeet = True
    while yeet:
        command = input("press q to exit\n"
                        "press s to search\n"
                        "What would you like to do?\n")
        if command == "q":
            break
        elif command == "s":
            search = SearchEngine(directory, import_stopwords("stop_words.txt", HashTableLinear()))
        else:
            print("that is not a valid command\n")
            continue
        new_query = [input("what would you like to search?\n")]
        query_string = search.parse_words(new_query)
        search.search(query_string)


if __name__ == '__main__':
    # execute main() function
    main()
