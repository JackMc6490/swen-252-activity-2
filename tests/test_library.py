import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from library import library
from library import patron
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.library = library.Library()
        with open('tests_data/ebooks.txt', 'r') as source:
            self.books_data = json.loads(source.read())

    def test_is_ebook_return_true(self):
        self.assertTrue(self.library.is_ebook('Aprendendo Python'))

    def test_is_ebook_return_false(self):
        self.assertFalse(self.library.is_ebook('War and Peace'))

    def test_get_ebooks_count(self):
        self.assertEqual(self.library.get_ebooks_count('Aprendendo Python'), 8)

    def test_is_book_by_author_true(self):
        self.library.api.books_by_author = Mock(return_value={'Aprendendo Python','War and Peacse'})
        self.assertTrue(self.library.is_book_by_author('Bob','Aprendendo Python'))

    def test_is_book_by_author_false(self):
        self.library.api.books_by_author = Mock(return_value={'Aprendendo Python','War and Peace'})
        self.assertFalse(self.library.is_book_by_author('Bob','Old Yeller'))

    def test_get_languages_for_book(self):
        self.library.api.get_book_info = Mock(return_value=[{'language': 'a'}])
        self.assertEqual(self.library.get_languages_for_book('Aprendendo Python'),{'a'})


        



    
    
    
