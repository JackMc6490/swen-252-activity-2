import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from library import library
from library import patron
import json

class TestLibrary(unittest.TestCase):
    
    #loads test ebook data
    def setUp(self):
        self.library = library.Library()
        with open('tests_data/ebooks.txt', 'r') as source:
            self.books_data = json.loads(source.read())
   

    #is_ebook() tests

    #Testing is_ebook() w/ book in test data
    def test_is_ebook_return_true(self):
        self.library.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.library.is_ebook('Aprendendo Python'))

    #Testing is_ebook() w/ book not in test data
    def test_is_ebook_return_false(self):
        self.library.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertFalse(self.library.is_ebook('War and Peace'))


    #Testing get_ebooks_count() w/ mock date
    def test_get_ebooks_count(self):
        self.library.api.get_ebooks = Mock(return_value=[{'title': 'Aprendendo Python', 'ebook_count': 3},{'title': 'Aprendendo Python', 'ebook_count': 4}])
        self.assertEqual(self.library.get_ebooks_count('Aprendendo Python'), 7)

    #is_book_by_author() tests

    #Testing is_book_by author when book is in mock data set
    def test_is_book_by_author_true(self):
        self.library.api.books_by_author = Mock(return_value={'Aprendendo Python','War and Peacse'})
        self.assertTrue(self.library.is_book_by_author('Bob','Aprendendo Python'))
    
    #Testing is_book_by author when book is not in mock data set
    def test_is_book_by_author_false(self):
        self.library.api.books_by_author = Mock(return_value={'Aprendendo Python','War and Peace'})
        self.assertFalse(self.library.is_book_by_author('Bob','Old Yeller'))

    #Testing get_langauges_for_book() w/ mock data 
    def test_get_languages_for_book(self):
        self.library.api.get_book_info = Mock(return_value=[{'language': 'a'},{'title':'A cool book'},{'publish_year':1984}])
        self.assertEqual(self.library.get_languages_for_book('Aprendendo Python'),{'a'})


    #is_patron_registered() tests

    #Testing is_patron_registered() when retrieve_patron() returns the patron
    def test_is_patron_registered_true(self):
        testpatron = patron.Patron("Billy","Bob",12,"bb12")
        self.library.db.retrieve_patron = Mock(return_value=testpatron)
        self.assertTrue(self.library.is_patron_registered(testpatron))

    #Testing is_patron_registered() when retrieve_patron() returns False
    def test_is_patron_registered_false(self):
        testpatron = patron.Patron("Billy","Bob",12,"bb12")
        self.library.db.retrieve_patron = Mock(return_value=False)
        self.assertFalse(self.library.is_patron_registered(testpatron))


    #Testing borrow_book() properly calls all functions
    def test_borrow_book(self):
        testpatron = patron.Patron("Billy","Bob",12,"bb12")
        testpatron.add_borrowed_book = Mock()  
        self.library.db.update_patron = Mock()
        self.library.borrow_book('Aprendendo Python',testpatron)
        self.library.db.update_patron.assert_called()
        testpatron.add_borrowed_book.assert_called()
    
    #Testing return_borrowed_book() properly calls all functions
    def test_return_borrowed_book(self):
        testpatron = patron.Patron("Billy","Bob",12,"bb12")
        testpatron.return_borrowed_book = Mock()  
        self.library.db.update_patron = Mock()
        self.library.return_borrowed_book('Aprendendo Python',testpatron)
        self.library.db.update_patron.assert_called()
        testpatron.return_borrowed_book.assert_called()

    #is_borrowed_book() tests

    #testing is_borrowed_book() when the book is borrowed
    def test_is_book_borrowed_true(self):
        testpatron = patron.Patron("Billy","Bob",12,"bb12")
        testpatron.get_borrowed_books = Mock(return_value={'aprendendo python','war and peace','horton hears a who'})
        self.assertTrue(self.library.is_book_borrowed('Aprendendo Python',testpatron))

    #testing is_borrowed_book() when the book is not borrowed
    def test_is_book_borrowed_false(self):
        testpatron = patron.Patron("Billy","Bob",12,"bb12")
        testpatron.get_borrowed_books = Mock(return_value={'aprendendo python','war and peace','horton hears a who'})
        self.assertFalse(self.library.is_book_borrowed('Percy Jackson and the Lighting Thief',testpatron))


    #register_patron tests

    #testing register_patron when insert_patron returns the id
    def test_register_patron_success(self):
        self.library.db.insert_patron = Mock(return_value=12)
        self.assertEqual(self.library.register_patron("Billy","Bob",37,"12"),12)

    #testing register_patron when insert_patron returns None
    def test_register_patron_failure(self):
        self.library.db.insert_patron = Mock(return_value=None)
        self.assertEqual(self.library.register_patron("Billy","Bob",37,"12"),None)


        



    
    
    
