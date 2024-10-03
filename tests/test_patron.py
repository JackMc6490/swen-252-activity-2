import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from library import patron
import json

class TestPatron(unittest.TestCase):

    def setUp(self):
        self.patron = patron.Patron("John","Doe",67,30)
        self.patron.add_borrowed_book('The Giving Tree')

    def test_invalid_name(self):
        try:
            badpatron = patron.Patron("Bob123","Jones",21,137)
            return False
        except:
            return True

    def test_add_borrowed_book(self):
        self.patron.add_borrowed_book("War and Peace")
        if "War and Peace" in self.patron.get_borrowed_books():
            return True
        else:
            return False
        
    def test_add_borrowed_book_already_borrowed(self):
        self.patron.add_borrowed_book('The Giving Tree')
        count = 0
        for book in self.patron.get_borrowed_books():
            if(book == 'the giving tree'):
                count+=1;
        self.assertEqual(count,1)

        
    def test_return_borrowed_book(self):
        self.patron.return_borrowed_book('The Giving Tree')
        if 'The Giving Tree' in self.patron.get_borrowed_books():
            return False
        else:
            return True
        
    def test_equal(self):
        self.assertEqual(self.patron,self.patron)

    def test_not_equal(self):
        comparepatron = patron.Patron("Bob","Jones",21,137)
        self.assertNotEqual(self.patron,comparepatron)

    def test_get_fname(self):
        self.assertEqual(self.patron.get_fname(),"John")

    def test_get_lname(self):
        self.assertEqual(self.patron.get_lname(),"Doe")

    def test_get_age(self):
        self.assertEqual(self.patron.get_age(),67)
    
    def test_get_id(self):
        self.assertEqual(self.patron.get_memberID(),30)


    
    

