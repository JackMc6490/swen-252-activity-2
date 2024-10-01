import json
import unittest
import library.ext_api_interface as EAI

from unittest.mock import Mock
class TestBooksAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.books_api = EAI.Books_API()
        with open('tests_data/mock_requests.json', 'r') as source:
            cls.mock_requests = json.loads(source.read())
        cls.books_api.make_request = Mock(return_value=cls.mock_requests)
        cls.books_api.is_book_available = Mock()
        cls.books_api.books_by_author = Mock()
        cls.books_api.get_book_info = Mock()
    
        


    def test_make_request(self):
        # Setup
        url = "http://openlibrary.org/search.json?q=Harry%20Potter"
        self.books_api.make_request.return_value = self.mock_requests[url]

        # Invoke
        result = self.books_api.make_request(url)

        # Assert
        self.assertTrue(bool(result))
        self.assertIn('docs', result)
        self.assertGreater(result['numFound'], 0)

    def test_is_book_available(self):
        # Setup
        book = "Harry Potter and the Sorcerer's Stone"
        self.books_api.is_book_available.return_value = self.mock_requests['https://openlibrary.org/search.json?q=Harry%20Potter%20and%20the%20Sorcerer%27s%20Stone']

        # Invoke
        result = self.books_api.is_book_available(book)

        # Assert
        self.assertTrue(result)

    def test_books_by_author(self):
        # Setup
        author = "Ray Bradbury"
        self.books_api.books_by_author.return_value = self.mock_requests['https://openlibrary.org/search.json?author=Ray%20Bradbury']

        # Invoke
        result = self.books_api.books_by_author(author)

        # Assert
        self.assertGreater(len(result), 0)
        self.assertIn("Fahrenheit 451", result)
        self.assertIn("The Martian Chronicles", result)

    def test_get_book_info(self):
        # Setup
        book = "The Great Gatsby"
        self.books_api.get_book_info.return_value = self.mock_requests['https://openlibrary.org/search.json?q=The%20Great%20Gatsby']

        # Invoke
        result = self.books_api.get_book_info(book)

        # Assert
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]['title'], "The Great Gatsby")
        self.assertIn('Macmillan Pub. Co.', result[0]['publisher'])
        self.assertIn(1925, result[0]['publish_year'])

    def test_get_book_info_no_results(self):
        # Setup
        book = "A Rediculously Long Title That Doesn't Exist. If it does exist, it's a coincidence. I swear."
        self.books_api.get_book_info.return_value = self.mock_requests['https://openlibrary.org/search.json?q=A%20Rediculously%20Long%20Title%20That%20Doesn%27t%20Exist.%20If%20it%20does%20exist%2C%20it%27s%20a%20coincidence.%20I%20swear.']
        # Invoke
        result = self.books_api.get_book_info(book)

        # Assert
        self.assertEqual(len(result), 0)

    def test_make_request_no_results(self):
        # Setup
        url = "http://openlibrary.org/search.json?q=A Rediculously Long Title That Doesn't Exist. If it does exist, it's a coincidence. I swear."
        self.books_api.make_request.return_value = self.mock_requests[url]
        # Invoke
        result = self.books_api.make_request(url)

        # Assert
        self.assertEqual(result['numFound'], 0)

    def test_is_book_available_no_results(self):
        # Setup
        book = "A Rediculously Long Title That Doesn't Exist. If it does exist, it's a coincidence. I swear."
        self.books_api.is_book_available.return_value = self.mock_requests['https://openlibrary.org/search.json?q=A%20Rediculously%20Long%20Title%20That%20Doesn%27t%20Exist.%20If%20it%20does%20exist%2C%20it%27s%20a%20coincidence.%20I%20swear.']
        # Invoke
        result = self.books_api.is_book_available(book)

        # Assert
        self.assertFalse(result)

