#!/usr/bin/env python
import re
import collections
import requests
import sys

# TODO Add user input statement for pageid and number of top K frequencies to print
page_id = "21721040"
num_of_top_words = 5


web_content = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=extracts&pageids={}&explaintext&format=json'.format(page_id))

word_list = re.sub(r'\.', " ", web_content.json()['query']['pages'][page_id]['extract']).split()
word_list = [word for word in [re.sub(r'[,.\"\';:()]$', '', word) for word in word_list] if len(word) >= 4]
frequencies = collections.Counter(word_list).most_common()

# TODO kachra saaf karne

i = 0
result = {}
for frequency in frequencies:
    if str(frequency[1]) in result:
        result[str(frequency[1])] = result[str(frequency[1])] + ", " + str(frequency[0])
    else:
        if i < num_of_top_words:
            result[str(frequency[1])] = str(frequency[0])
            num_of_top_words += 1

print(result)