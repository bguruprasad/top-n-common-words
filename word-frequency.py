#!/usr/bin/env python
import re
from collections import Counter, OrderedDict
import requests
import sys


# Global Variables
PYTHON_MAJOR_VERSION = sys.version[0]
WIKI_PAGE_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&pageids={}&explaintext&format=json"


# Helper Functions
def get_user_inputs():
    """
    Helper function to get user inputs for page_id to fetch wiki content from and words to print
    :return wiki_page_id: page_id for wiki
    :return words_to_print: top n frequent words to print
    """
    # TODO Add exception handling
    if PYTHON_MAJOR_VERSION == '3':
        wiki_page_id = str(input(" # Please Enter Wiki Page Id to fetch content from: "))
        num_of_top_words = str(input(" # Please Enter how many words to Frequent words to print: "))
    elif PYTHON_MAJOR_VERSION == '2':
        wiki_page_id = str(raw_input(" # Please Enter Wiki Page Id to fetch content from: "))
        num_of_top_words = str(raw_input(" # Please Enter how many top Frequent words to print: "))

    return wiki_page_id, num_of_top_words


def get_wiki_content(wiki_page_id):
    """
    Helper function to get wiki page content for page_id provided.
    :param wiki_page_id: page_id to fetch json content from
    :return wiki_content: json object for wiki page content
    """
    try:
        wiki_content = requests.get(WIKI_PAGE_URL.format(wiki_page_id))
        wiki_content.raise_for_status()  # This will raise the exception if status_code is not 200
        return wiki_content.json()
    except requests.exceptions.HTTPError as http_exception:
        print(" [ EXCEPTION : HTTP Error Occurred : {} ]".format(str(http_exception)))
    except requests.exceptions.ConnectionError as connection_exception:
        print(" [ EXCEPTION : Error fetching web content : {} ]".format(str(connection_exception)))
    except requests.exceptions.InvalidURL as invalid_url_exception:
        print(" [ EXCEPTION : HTTP Error Occurred : {} ]".format(str(invalid_url_exception)))
    except requests.exceptions.RequestException as request_exception:
        print(" [ EXCEPTION : Error Occurred while serving request : {} ]".format(str(request_exception)))
    except KeyboardInterrupt as keyboard_exception:
        print(" [ EXCEPTION : Execution Aborted : {} ]".format(str(keyboard_exception)))
    except Exception as generic_exception:
        print(" [ EXCEPTION : Generic Exception Occurred : {} ]".format(str(generic_exception)))


def convert_json_to_word_list(wiki_content_json, wiki_page_id):
    """
    Helper function to extract and convert.
    :param wiki_content_json: content json to extract page content from
    :return word_list: word_list with all required filters
    """
    try:
        # extract the the content from query.pages.[wiki_page_id].extract, replace .() with space and split
        #word_list = re.sub(r'[.()\[\]\{\}\<\>:\/]', " ", wiki_content_json['query']['pages'][wiki_page_id]['extract']).split()
        word_list = re.sub(r'[^\w| ]', " ", wiki_content_json['query']['pages'][wiki_page_id]['extract']).split()

        # strip the spliced word for possible punctuations, discard the word > 4 char length.
        word_list = [word for word in word_list if len(word) >= 4 and not word.isnumeric()]
        return word_list
    except Exception as e:
        print(" [ EXCEPTION : Generic Exception Occurred : {} ]".format(str(e)))


def get_top_n_frequent_words(word_list, num_of_top_words):
    """
    Helper function to generate list of frequent words and return requested top n words
    :param word_list: word_list to finding frequencies
    :param num_of_top_words: number of top n words to print
    :return: dictionary containing { frequencies: [word_list] }
    """
    try:
        # find the frequencies of the word using collections.Counter().most_common()
        frequencies = Counter(word_list).most_common()

        # find the top n frequent words
        i = 0
        required_words = OrderedDict()
        for frequency in frequencies:
            if str(frequency[1]) in required_words:
                required_words[str(frequency[1])].append(str(frequency[0]))
            else:
                if i < num_of_top_words:
                    required_words[str(frequency[1])] = [str(frequency[0])]
                    i += 1

        return required_words
    except Exception as e:
        print(" [ EXCEPTION : Generic Exception Occurred : {} ]".format(str(e)))


# TODO Add user input statement for pageid and number of top K frequencies to print
page_id = "21721040"
num_of_top_word = 5

if __name__ == '__main__':
    print("[ FINDING TOP N MOST FREQUENT WORDS ]")
    wiki_page_id, num_of_top_words = "21721047", "7"#get_user_inputs()
    wiki_content_json = get_wiki_content(wiki_page_id)
    word_list = convert_json_to_word_list(wiki_content_json, wiki_page_id)
    result = get_top_n_frequent_words(word_list, int(num_of_top_words))

    print("\nURL being called: {}".format(WIKI_PAGE_URL.format(wiki_page_id)))
    print("\nTitle : {}".format(wiki_content_json['query']['pages'][wiki_page_id]['title']))

    if len(result) < int(num_of_top_words):
        num_of_top_words = len(result)

    print("Top {} Words:".format(str(num_of_top_words)))
    for frequency, words in result.items():
        print(" - {} {}".format(frequency, ', '.join(words)))
