#!/usr/bin/env python
import json
import unittest
from collections import OrderedDict

import requests

import word_frequency


class WordFrequencyTest(unittest.TestCase):
    wiki_page_id = str(21721040)  # test wiki page id

    def test_get_wiki_content(self):
        """
        Test for verifying json object is being returned.
        """
        self.assertEqual(bool(word_frequency.get_wiki_content(self.wiki_page_id)), True)

    def test_valid_extract_key_present(self):
        """
        Test for validating if json object have valid extract key present
        """
        self.assertTrue(word_frequency.get_wiki_content(self.wiki_page_id)['query']['pages'][self.wiki_page_id]['extract'])

    def test_valid_title_key_present(self):
        """
        Test for validating if json object have valid title key present
        """
        self.assertTrue(word_frequency.get_wiki_content(self.wiki_page_id)['query']['pages'][self.wiki_page_id]['title'])

    """
    @mock.patch('word_frequency.requests.get')
    def test_request_http_error(self, mock_get_wiki_content):
        #Test for behaviour on http error for get_wiki_content function
        
        mock_response = mock.Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_get_wiki_content.return_value = mock_response
        with self.assertRaises(requests.exceptions.HTTPError):
            word_frequency.get_wiki_content(self.wiki_page_id)
    """
    def test_convert_json_to_word_list(self):
        """
        Test to validate correct word list is being returned
        :return:
        """
        word_list = self._get_word_list_from_sample_json()
        # For testing, testing with slice of excepted word_list
        word_list_slice = ['Stack', 'Overflow', 'question', 'answer', 'site', 'professional', 'enthusiast', 'programmers', 'privately', 'held', 'website', 'flagship', 'site', 'Stack', 'Exchange', 'Network']

        self.assertListEqual(word_list[:16], word_list_slice)

    def _get_word_list_from_sample_json(self):
        """
        Helper function to get word_list from sample data
        :return: word_list
        """
        with open('sample_wiki_content.json') as wiki_json_file:
            wiki_json = json.load(wiki_json_file)
        word_list = word_frequency.convert_json_to_word_list(wiki_json, self.wiki_page_id)
        return word_list

    def test_get_top_n_frequent_words(self):
        """
        Test to validate correct top n words are returned.
        """
        word_list = self._get_word_list_from_sample_json()
        original_result = word_frequency.get_top_n_frequent_words(word_list, 5)
        excepted_result = OrderedDict()
        for pair in [('20', ['Stack', 'questions']), ('17', ['Overflow']), ('12', ['users']), ('11', ['that', 'site']), ('10', ['question'])]:
            excepted_result[pair[0]] = pair[1]

        self.assertDictEqual(original_result, excepted_result)


if __name__ == "__main__":
    unittest.main()
