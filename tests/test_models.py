import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.setup import create_tables
from database.connection import get_db_connection

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_tables()

    def setUp(self):
        # Reset database state
        conn = get_db_connection()
        with conn:
            conn.execute("DELETE FROM authors")
            conn.execute("DELETE FROM magazines")
            conn.execute("DELETE FROM articles")

    def test_author_initialization(self):
        author = Author(1, "Justin")
        self.assertEqual(author.id, 1)
        self.assertEqual(author.name, "Justin")

    # Add more tests here

if __name__ == "__main__":
    unittest.main()
