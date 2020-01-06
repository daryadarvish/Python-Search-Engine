# Python Search Engine

This is a basic search engine that I created in CPE 202 (Data Structures).  You can run this program by downloading the reppository as a zip file and running the file name SearchEngine.py

The program will first ask which directory you would like to search.  If you type "docs", it will search through text files in the directory named "docs" and count the number of times a given word appears.

The program will then store these frequencies in a hashtable, where the values stored in the hashtable are a key value pair.  The key is the word (ex. "data"), and the value is a hashtable.  The hashtable stored as a value has key value pairs where the key is the name of the text file (ex the word is found and the value is the number of occurences of the word in that text file.

This hashtable is an attribute of SearchEngine class called term_freqs.  Other attributes of SearchEngine class are doc_length, which stores the number of words in each text file, and stopwords which is a list of words that are commonly used (ex. the, is, at) that the program does not search through when parsing text files.

Finally, the program will prompt the user for a search query, and will return the names of documents where the search query occures, as well as a normalized score that ranks which documents will be displayed first.

Let me know if you have any questions :)
