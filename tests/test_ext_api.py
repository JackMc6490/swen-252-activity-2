import json
import unittest
import requests
import library.ext_api_interface as EAI

from unittest.mock import Mock
class TestBooksAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.books_api = EAI.Books_API()
        with open('tests_data/mock_requests.json', 'r') as source:
            cls.mock_requests = json.loads(source.read())


    def setUp(self):
        # make a Response object with the mock data
        def mock_get(url):
            response = requests.Response()
            response.status_code = self.mock_requests[url]["status_code"]
            response.__setattr__("_content", self.mock_requests[url])
            return response
        requests.get = mock_get
        requests.Response.json = (lambda self: self._content["json"])
        self.books_api = EAI.Books_API()

    
        


    def test_make_request(self):
        # Setup
        url = "http://openlibrary.org/search.json?q=Harry Potter"

        # Invoke
        result = self.books_api.make_request(url)

        # Assert
        self.assertTrue(bool(result))
        self.assertIn('docs', result)
        self.assertGreater(result['numFound'], 0)

    def test_make_request_no_connection(self):
        # Setup
        url = "http://openlibrary.org/search.json?q=Harry Potter"
        requests.get = Mock(side_effect=requests.ConnectionError)

        # Invoke
        result = self.books_api.make_request(url)

        # Assert
        self.assertIsNone(result)

    def test_make_request_bad_status_code(self):
        # Setup
        url = "http://openlibrary.org/search.jso"
        # Invoke with bad status code
        result = self.books_api.make_request(url)


        # Assert
        self.assertIsNone(result)

    def test_is_book_available(self):
        # Setup
        book = "Harry Potter and the Sorcerer's Stone"

        # Invoke
        result = self.books_api.is_book_available(book)

        # Assert
        self.assertTrue(result)

    def test_books_by_author_bad_json(self):
        # Setup
        book = "Harry Potter and the Sorcerer's Stone"
        self.books_api.make_request = Mock(return_value=None)

        # Invoke
        result = self.books_api.books_by_author(book)

        # Assert
        self.assertEquals(result, [])


    def test_books_by_author(self):
        # Setup
        author = "Ray Bradbury"

        # Invoke
        result = self.books_api.books_by_author(author)

        # Assert
        self.assertGreater(len(result), 0)
        self.assertIn("Fahrenheit 451", result)
        self.assertIn("The Martian Chronicles", result)

    def test_get_book_info(self):
        # Setup
        book = "The Great Gatsby"

        # Invoke
        result = self.books_api.get_book_info(book)

        # Assert
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]['title'], "The Great Gatsby")
        self.assertIn('Macmillan Pub. Co.', result[0]['publisher'])
        self.assertIn(1925, result[0]['publish_year'])
    
    def test_get_book_info_bad_json(self):
        # Setup
        book = "The Great Gatsby"
        self.books_api.make_request = Mock(return_value=None)

        # Invoke
        result = self.books_api.get_book_info(book)

        # Assert
        self.assertEquals(result, [])

    def test_get_book_info_no_results(self):
        # Setup
        book = "A Rediculously Long Title That Doesn't Exist. If it does exist, it's a coincidence. I swear."
       
        # Invoke
        result = self.books_api.get_book_info(book)

        # Assert
        self.assertEqual(len(result), 0)

    def test_is_book_available_no_results(self):
        # Setup
        book = "A Rediculously Long Title That Doesn't Exist. If it does exist, it's a coincidence. I swear."
        # Invoke
        result = self.books_api.is_book_available(book)

        # Assert
        self.assertFalse(result)

    def test_get_ebooks(self):
        # Setup
        # Invoke
        result = self.books_api.get_ebooks("The Great Gatsby")

        # Assert
        self.assertGreater(len(result), 0)
        self.assertGreaterEqual(result[0]["ebook_count"], 1)

    def test_get_ebooks_no_results(self):
        # Setup
        # Invoke
        result = self.books_api.get_ebooks("A Rediculously Long Title That Doesn't Exist. If it does exist, it's a coincidence. I swear.")

        # Assert
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])
    
    def test_get_ebooks_bad_json(self):
        # Setup
        self.books_api.make_request = Mock(return_value=None)
        # Invoke
        result = self.books_api.get_ebooks("The Great Gatsby")

        # Assert
        self.assertEqual(result, [])

