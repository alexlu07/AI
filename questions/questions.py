import nltk
import sys
import os
import string
import math
from collections import defaultdict

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    print("Loading files...")
    result = {}
    for document in os.listdir(directory):
        with open(os.path.join(directory, document), "r") as f:
            result[document] = f.read()

    return result

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = [word.lower() for word in nltk.tokenize.word_tokenize(document)]
    results = []
    for word in words.copy():
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            results.append(word)

    return results


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    print("Extracting all words...")
    words = set()
    for document in documents:
        words.update(documents[document])

    print("Calculating IDFs...")
    idfs = {}
    for word in words:
        f = sum(word in documents[document] for document in documents)
        idf = math.log(len(documents) / f)
        idfs[word] = idf

    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    print("Calculating top files...")
    tf = {}
    for document in files:
        tf[document] = defaultdict(lambda: 0)
        for word in files[document]:
            tf[document][word] += 1

    tfidf = [[document, sum([tf[document][word] * idfs[word] for word in query if word in files[document]])] for document in files]
    return [i[0] for i in sorted(tfidf, key=lambda x: x[1], reverse=True)[:n]]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    print("Calculating best sentences...")
    sentences = [[sentence, sum([idfs[word] for word in query if word in sentences[sentence]])] for sentence in sentences]
    sentences = sorted(sentences, key=lambda x: x[1], reverse=True)

    index = 0
    new_sentences = []
    while index < len(sentences)-1:
        temp_list = [sentences[index]]
        for offset in range(index+1, len(sentences)-index):
            if sentences[index][1] == sentences[index+offset][1]:
                temp_list.append(sentences[index+offset])
                continue
            break
        index += offset
        new_sentences.append(sorted(temp_list, key=lambda x: sum([word in query for word in x[0].split()]) / len(x[0].split()), reverse=True))

    new_sentences = [sentence for x in new_sentences for sentence in x]
    return [x[0] for x in new_sentences[:n]]

if __name__ == "__main__":
    main()
