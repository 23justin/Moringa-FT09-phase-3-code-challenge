from database.connection import get_db_connection
from models.author import Author  # Import Author class
from models.magazine import Magazine  # Import Magazine class

class Article:
    def __init__(self, id, title, author, magazine):
        if not isinstance(id, int):
            raise TypeError("id must be an integer")
        if not isinstance(title, str) or len(title) < 5 or len(title) > 50:
            raise ValueError("title must be a string between 5 and 50 characters")
        if not isinstance(author, Author):
            raise TypeError("author must be an instance of Author")
        if not isinstance(magazine, Magazine):
            raise TypeError("magazine must be an instance of Magazine")

        self._id = id
        self._title = title
        self._author = author
        self._magazine = magazine
        self.save()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    def save(self):
        conn = get_db_connection()
        with conn:
            conn.execute("INSERT OR REPLACE INTO articles (id, title, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                         (self._id, self._title, self._author.id, self._magazine.id))

    def delete(self):
        conn = get_db_connection()
        with conn:
            conn.execute("DELETE FROM articles WHERE id = ?", (self._id,))
