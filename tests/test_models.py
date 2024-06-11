# tests/test_models.py

import unittest
from models.author import Author
from models.magazine import Magazine
from models.article import Article
from database.connection import get_db_connection

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        conn = get_db_connection()
        with conn:
            conn.execute("DROP TABLE IF EXISTS authors")
            conn.execute("DROP TABLE IF EXISTS magazines")
            conn.execute("DROP TABLE IF EXISTS articles")
            conn.execute("""
                CREATE TABLE authors (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE magazines (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE articles (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    author_id INTEGER,
                    magazine_id INTEGER,
                    FOREIGN KEY (author_id) REFERENCES authors (id),
                    FOREIGN KEY (magazine_id) REFERENCES magazines (id)
                )
            """)

    def setUp(self):
        conn = get_db_connection()
        with conn:
            conn.execute("DELETE FROM authors")
            conn.execute("DELETE FROM magazines")
            conn.execute("DELETE FROM articles")

    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_author_creation_invalid(self):
        with self.assertRaises(ValueError):
            Author(2, "")
        with self.assertRaises(TypeError):
            Author("2", "Jane Doe")

    def test_author_deletion(self):
        author = Author(1, "John Doe")
        author.delete()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM authors WHERE id = ?", (1,))
        self.assertIsNone(cur.fetchone())

    def test_author_articles(self):
        author = Author(3, "Alice")
        magazine = Magazine(1, "Tech Weekly", "Technology")
        article = Article(1, "Tech Insights", "Content", author.id, magazine.id)
        articles = author.articles()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['title'], "Tech Insights")

    def test_author_magazines(self):
        author = Author(4, "Bob")
        magazine1 = Magazine(2, "Tech Weekly", "Technology")
        magazine2 = Magazine(3, "Health Weekly", "Health")
        Article(2, "Tech Article", "Content", author.id, magazine1.id)
        Article(3, "Health Article", "Content", author.id, magazine2.id)
        magazines = author.magazines()
        self.assertIn("Tech Weekly", magazines)
        self.assertIn("Health Weekly", magazines)

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.content, "Test Content")
        self.assertEqual(article.id, 1)
        self.assertEqual(article._author_id, 1)
        self.assertEqual(article._magazine_id, 1)

    def test_article_creation_invalid(self):
        with self.assertRaises(ValueError):
            Article(4, "Shrt", "Content", 1, 1)
        with self.assertRaises(ValueError):
            Article(5, "Valid Title", "", 1, 1)

    def test_article_deletion(self):
        article = Article(6, "Delete Me", "Content", 1, 1)
        article.delete()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE id = ?", (6,))
        self.assertIsNone(cur.fetchone())

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")

    def test_magazine_creation_invalid(self):
        with self.assertRaises(ValueError):
            Magazine(4, "T", "Technology")
        with self.assertRaises(ValueError):
            Magazine(5, "Valid Name", "")

    def test_magazine_deletion(self):
        magazine = Magazine(2, "Delete Me", "Technology")
        magazine.delete()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM magazines WHERE id = ?", (2,))
        self.assertIsNone(cur.fetchone())

    def test_magazine_articles(self):
        magazine = Magazine(3, "Tech Monthly", "Technology")
        author = Author(5, "Charlie")
        Article(7, "Monthly Review", "Content", author.id, magazine.id)
        articles = magazine.articles()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['title'], "Monthly Review")

    def test_magazine_contributors(self):
        magazine = Magazine(4, "Tech Quarterly", "Technology")
        author1 = Author(6, "Dana")
        author2 = Author(7, "Eli")
        Article(8, "Quarterly Tech", "Content", author1.id, magazine.id)
        Article(9, "Quarterly Insights", "Content", author2.id, magazine.id)
        contributors = magazine.contributors()
        self.assertIn("Dana", [contrib.name for contrib in contributors])
        self.assertIn("Eli", [contrib.name for contrib in contributors])

if __name__ == "__main__":
    unittest.main()


