import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from library import patron
import json
import re

class TestPatron(unittest.TestCase):

    #Creates a test patron and adds one borrowed book
    def setUp(self):
        self.patron = patron.Patron("John","Doe",67,30)
        self.patron.add_borrowed_book('The Giving Tree')


    def test_creation(self):
        re.search = Mock(return_value=False)
        patron2 = patron.Patron("Jane","Doe",67,30)
        re.search.assert_any_call('\d',"Jane")
        
    #Test to confirm you can't have numbers in a patrons name
    def test_invalid_name(self):
        try:
            badpatron = patron.Patron("Bob123","Jones",21,137)
            return False
        except:
            return True

    #Testing borrowing a book
    def test_add_borrowed_book(self):
        self.patron.add_borrowed_book("War and Peace")
        if "War and Peace" in self.patron.get_borrowed_books():
            return True
        else:
            return False
    ##Testing borrowing a boom that has already been borrowed  
    def test_add_borrowed_book_already_borrowed(self):
        self.patron.add_borrowed_book('The Giving Tree')
        count = 0
        for book in self.patron.get_borrowed_books():
            if(book == 'the giving tree'):
                count+=1
        self.assertEqual(count,1)

    #Testing returning a book 
    def test_return_borrowed_book(self):
        self.patron.return_borrowed_book('The Giving Tree')
        if 'The Giving Tree' in self.patron.get_borrowed_books():
            return False
        else:
            return True
        
    #equals and not equals tests

    def test_equal(self):
        self.assertEqual(self.patron,self.patron)

    def test_not_equal(self):
        comparepatron = patron.Patron("Bob","Jones",21,137)
        self.assertNotEqual(self.patron,comparepatron)


    #getter tests just for code coverage

    def test_get_fname(self):
        self.assertEqual(self.patron.get_fname(),"John")

    def test_get_lname(self):
        self.assertEqual(self.patron.get_lname(),"Doe")

    def test_get_age(self):
        self.assertEqual(self.patron.get_age(),67)
    
    def test_get_id(self):
        self.assertEqual(self.patron.get_memberID(),30)


    
    

