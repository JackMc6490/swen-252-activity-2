"""
Filename: test_library_db_interface.py
Description: Testing module for the Library_DB class
"""

import unittest
from unittest.mock import Mock, call
from library import library_db_interface

class TestLibrary_DB(unittest.TestCase):
    
    test_data = {
        'fname': 'julian',
        'lname': 'juliard',
        'age': 123,
        'memberID': 1,
        'borrowed_books': []
    }
    
    def setUp(self):
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
    
    
        
        