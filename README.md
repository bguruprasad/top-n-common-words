# Find Top N Word Frequency

Program to fetch a Wikipedia page and report the top n words on that page.

The user inputs to the program are `page_id` and `n` (number of top frequent words to print).

The fixed URL to fetch a page from Wikipedia is
`https://en.wikipedia.org/w/api.php?action=query&prop=extracts&pageids=<PAGE
ID>&explaintext&format=json`

---

## Python Requirements

The program is built and tested on `Python2.7` & `Python3.7`. This program uses the `requests` library for URL calls. The library can be installed by executing following command from program root directory as
```
pip install -i requirements.txt
```

## Python Unit Test

To Execute the python unit test, execute following command in program root directory.
```
python word_frequency_test.py
```

---

## Program Execution Example

```
> python word_frequency.py
[ FINDING TOP N MOST FREQUENT WORDS ]
# Please Enter Wiki Page Id to fetch content from (accepts digits only): 21721040
# Please Enter how many top Frequent words to print (accepts digits only): 5

URL being called: https://en.wikipedia.org/w/api.php?action=query&prop=extracts&pageids=21721040&explaintext&format=json

Title : Stack Overflow
Top 5 Words:
 - 20 Stack, questions
 - 17 Overflow
 - 12 users
 - 11 site, that
 - 10 question

```