#!/usr/bin/env python
import re
from collections import Counter, OrderedDict
import requests
import sys

# Global Variables
PYTHON_MAJOR_VERSION = sys.version[0]
WIKI_PAGE_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&pageids={}&explaintext&format=json"


def get_user_inputs():
    """
    Function to get user inputs for page_id to fetch wiki content from and words to print
    :return wiki_page_id: page_id for wiki
    :return words_to_print: top n frequent words to print
    """
    wiki_page_id, num_of_top_words = '', ''
    while not wiki_page_id.isnumeric():
        if PYTHON_MAJOR_VERSION == '3':
            wiki_page_id = str(input("# Please Enter Wiki Page Id to fetch content from (accepts digits only): "))
        elif PYTHON_MAJOR_VERSION == '2':
            wiki_page_id = str(raw_input("# Please Enter Wiki Page Id to fetch content from (accepts digits only): "))

    while not num_of_top_words.isnumeric():
        if PYTHON_MAJOR_VERSION == '3':
            num_of_top_words = str(input("# Please Enter how many words to Frequent words to print (accepts digits only): "))
        elif PYTHON_MAJOR_VERSION == '2':
            num_of_top_words = str(raw_input("# Please Enter how many top Frequent words to print (accepts digits only): "))

    return wiki_page_id, num_of_top_words


def get_wiki_content(wiki_page_url, wiki_page_id):
    """
    Function to get wiki page content for page_id provided.
    :param wiki_page_id: page_id to fetch json content from
    :return wiki_content: json object for wiki page content
    """
    wiki_json = {}
    try:
        wiki_content = requests.get(wiki_page_url.format(wiki_page_id))
        wiki_content.raise_for_status()  # This will raise the exception if status_code is not 200
        wiki_json = wiki_content.json()
    except requests.exceptions.HTTPError as http_exception:
        print("[ EXCEPTION : HTTP Error Occurred : {} ]".format(str(http_exception)))
    except requests.exceptions.ConnectionError as connection_exception:
        print("[ EXCEPTION : Error fetching web content : {} ]".format(str(connection_exception)))
    except requests.exceptions.InvalidURL as invalid_url_exception:
        print("[ EXCEPTION : HTTP Error Occurred : {} ]".format(str(invalid_url_exception)))
    except KeyboardInterrupt as keyboard_exception:
        print("[ EXCEPTION : Execution Aborted : {} ]".format(str(keyboard_exception)))
    except Exception as generic_exception:
        print("[ EXCEPTION : Generic Exception Occurred : {} ]".format(str(generic_exception)))
    finally:
        return wiki_json


def convert_json_to_word_list(wiki_content_json, wiki_page_id):
    """
    Function to extract and convert.
    :param wiki_content_json: content json to extract page content from
    :return word_list: word_list with all required filters
    """
    word_list = []
    try:
        # extract the the content from query.pages.[wiki_page_id].extract, replace .() with space and split
        word_list = re.sub(r'[^\w| ]', " ", wiki_content_json['query']['pages'][wiki_page_id]['extract']).split()

        # strip the spliced word for possible punctuations, discard the word > 4 char length.
        word_list = [word for word in word_list if len(word) >= 4 and not word.isnumeric()]
    except Exception as e:
        print("[ EXCEPTION : Generic Exception Occurred : {} ]".format(str(e)))
    finally:
        return word_list


def get_top_n_frequent_words(word_list, num_of_top_words):
    """
    Function to generate list of frequent words and return requested top n words
    :param word_list: word_list to finding frequencies
    :param num_of_top_words: number of top n words to print
    :return: dictionary containing { frequency: [word_list] }
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
        print("[ EXCEPTION : Generic Exception Occurred : {} ]".format(str(e)))
        sys.exit(1)


def check_valid_key_json(wiki_content_json, wiki_page_id):
    """
    Function to validate correct json keys are present.
    :param wiki_content_json: json content in which keys to be verify
    :param wiki_page_id: wiki page id
    :return: True if required keys are present, else False
    """
    is_key_valid = False
    try:
        if 'query' in wiki_content_json:
            if 'pages' in wiki_content_json['query']:
                if str(wiki_page_id) in wiki_content_json['query']['pages']:
                    if 'extract' in wiki_content_json['query']['pages'][str(wiki_page_id)]:
                        if 'title' in wiki_content_json['query']['pages'][str(wiki_page_id)]:
                            is_key_valid = True
                        else:
                            raise KeyError('query.pages.{}.title'.format(str(wiki_page_id)))
                    else:
                        raise KeyError('query.pages.{}.extract'.format(str(wiki_page_id)))
                else:
                    raise KeyError('query.pages.{}'.format(str(wiki_page_id)))
            else:
                raise KeyError('query.pages')
        else:
            raise KeyError('query')
    except KeyError as ke:
        print("[ EXCEPTION : Key does not exists : {} ]".format(str(ke)))
    except Exception as e:
        print("[ EXCEPTION : Generic Exception Occurred : {} ]".format(str(e)))
    finally:
        return is_key_valid


if __name__ == '__main__':
    try:
        print("[ FINDING TOP N MOST FREQUENT WORDS ]")
        wiki_page_id, num_of_top_words = get_user_inputs()

        if not wiki_page_id or not num_of_top_words:
            print('Proper input not provided, existing...')
            exit(1)

        print("\nURL being called: {}".format(WIKI_PAGE_URL.format(wiki_page_id)))

        wiki_content_json = get_wiki_content(WIKI_PAGE_URL, wiki_page_id)
        if not wiki_content_json:
            print('No JSON data return, existing...')
            exit(1)

        if not check_valid_key_json(wiki_content_json, wiki_page_id):
            print('Unable to proceed...Exiting...')
            exit(1)

        word_list = convert_json_to_word_list(wiki_content_json, wiki_page_id)

        if not word_list:
            print('No words in the web content, unable to proceed. Existing...')
            exit(1)

        result = get_top_n_frequent_words(word_list, int(num_of_top_words))

        if len(result) < int(num_of_top_words):
            print("\nFound only top {} frequent words instead of {}.".format(str(len(result)), num_of_top_words))
            num_of_top_words = len(result)

        print("\nTitle : {}".format(wiki_content_json['query']['pages'][wiki_page_id]['title']))

        print("Top {} Words:".format(str(num_of_top_words)))
        for frequency, words in result.items():
            print(" - {} {}".format(frequency, ', '.join(words)))
    except Exception as e:
        print("[ EXCEPTION : Generic Exception Occurred : {} ]".format(str(e)))