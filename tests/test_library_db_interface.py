"""
Filename: test_library_db_interface.py
Description: Testing module for the Library_DB class
"""

import unittest
from unittest.mock import Mock, call
from library import library_db_interface
from library.patron import Patron
from tinydb import TinyDB

class TestLibrary_DB(unittest.TestCase):
    
    test_data = {
        'fname': 'julian',
        'lname': 'juliard',
        'age': 123,
        'memberID': 1,
        'borrowed_books': []
    }
    
    def setUp(self):
        TinyDB.__init__ = Mock(return_value=None)
        TinyDB.close = Mock()
        self.db_interface = library_db_interface.Library_DB()
        
    def tearDown(self):
        self.db_interface.close_db()
        self.db_interface = None
        
    def test_insert_patron_none(self):
        
        # Mock calls
        self.db_interface.retrieve_patron = Mock()
        
        # invoke & test
        self.assertEqual(None, self.db_interface.insert_patron(None))
        self.db_interface.retrieve_patron.assert_not_called()
        
    def test_insert_patron(self):
        mock_patron = Mock()
        
        # Mock calls
        self.db_interface.retrieve_patron = Mock(return_value=None)
        self.db_interface.convert_patron_to_db_format = Mock(return_value=self.test_data)
        self.db_interface.db.insert = Mock(return_value=self.test_data['memberID'])
        
        # Invoke command
        ret_val = self.db_interface.insert_patron(mock_patron)
        
        # Test mock calls
        self.db_interface.retrieve_patron.assert_called()
        self.db_interface.convert_patron_to_db_format.assert_called()
        self.db_interface.db.insert.assert_called()
        
        # Test return value
        self.assertEqual(ret_val, self.test_data['memberID'])
        
    def test_insert_patron_collision(self):
        mock_patron = Mock()
        
        # Mock Calls
        mock_patron.get_memberID = Mock(return_value=2)
        self.db_interface.retrieve_patron = Mock(return_value=mock_patron)
        self.db_interface.convert_patron_to_db_format = Mock()
        
        # Invoke
        ret_val = self.db_interface.insert_patron(mock_patron)
        
        # Test Mock Calls
        self.db_interface.retrieve_patron.assert_called()
        mock_patron.get_memberID.assert_called()
        
        # Test return value
        self.assertEqual(ret_val, None)
    
    def test_get_patron_count(self):
        
        # Mock Call
        self.db_interface.db.all = Mock(return_value=[1,2,3,4])
        
        # Invoke
        ret_val = self.db_interface.get_patron_count()
        
        # Evaluate
        self.db_interface.db.all.assert_called()
        self.assertEqual(4, ret_val)
        
    def test_get_all_patrons(self):
        # Mock Call
        data = [1,2,3,4]
        self.db_interface.db.all = Mock(return_value=data)
        
        # Invoke
        ret_val = self.db_interface.get_all_patrons()
        
        # Evaluate
        self.db_interface.db.all.assert_called()
        self.assertEqual(data, ret_val)
        
    def test_update_patron_none(self):
        # Mock Call
        self.db_interface.convert_patron_to_db_format = Mock()
        
        # Invoke
        ret_val = self.db_interface.update_patron(None)
        
        # Evaluate
        self.db_interface.convert_patron_to_db_format.assert_not_called()
        self.assertEqual(ret_val, None)
        
    def test_update_patron(self):
        mock_patron = Mock()
        
        # Mock Call
        self.db_interface.convert_patron_to_db_format = Mock(return_value="fun")
        mock_patron.get_memberID = Mock(return_value=12)
        self.db_interface.db.update = Mock()
        
        # Invoke
        self.db_interface.update_patron(mock_patron)
        
        # Evaluate
        self.db_interface.db.update.assert_called()
        mock_patron.get_memberID.assert_called()
        self.db_interface.convert_patron_to_db_format.assert_called()
        
    def test_close_db(self):
        # Mock Call
        self.db_interface.db.close = Mock()
        
        #Invoke
        self.db_interface.close_db()
        
        # Evaluate
        self.db_interface.db.close.assert_called()
        
    def test_convert_patron_to_db_format(self):
        mock_patron = Mock()
        mock_patron.get_fname = Mock(return_value=self.test_data['fname'])
        mock_patron.get_lname = Mock(return_value=self.test_data['lname'])
        mock_patron.get_age = Mock(return_value=self.test_data['age'])
        mock_patron.get_memberID = Mock(return_value=self.test_data['memberID'])
        mock_patron.get_borrowed_books = Mock(return_value=self.test_data['borrowed_books'])
        
        # Invoke
        ret_val = self.db_interface.convert_patron_to_db_format(mock_patron)
        
        # Evaluate
        self.assertEqual(ret_val, self.test_data)
        
    def test_retrieve_patron(self):
        # Mock Call
        self.db_interface.db.search = Mock(return_value=[self.test_data])
        
        # Invoke
        ret_val = self.db_interface.retrieve_patron(self.test_data['memberID'])
        
        # Evaluate
        self.assertEqual(ret_val, Patron(
            self.test_data['fname'],
            self.test_data['lname'],
            self.test_data['age'],
            self.test_data['memberID']
        ))
        
        
    def test_retrieve_patron_not_in(self):
        # Mock Call
        self.db_interface.db.search = Mock(return_value=[])
        
        # Invoke
        ret_val = self.db_interface.retrieve_patron(self.test_data['memberID'])
        
        # Evaluate
        self.assertEqual(ret_val, None)