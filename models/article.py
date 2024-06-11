# models/article.py

from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        if not isinstance(id, int):
            raise TypeError("id must be an integer")
        if not isinstance(title, str) or len(title) < 5:
            raise ValueError("title must be a string with at least 5 characters")
        if not isinstance(content, str) or len(content) == 0:
            raise ValueError("content must be a non-empty string")
        self.id = id
        self.title = title
        self.content = content
        self._author_id = author_id
        self._magazine_id = magazine_id
        self.save()

    def save(self):
        conn = get_db_connection()
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO articles (id, title, content, author_id, magazine_id) VALUES (?, ?, ?, ?, ?)",
                (self.id, self.title, self.content, self._author_id, self._magazine_id)
            )

    def delete(self):
        conn = get_db_connection()
        with conn:
            conn.execute("DELETE FROM articles WHERE id = ?", (self.id,))
