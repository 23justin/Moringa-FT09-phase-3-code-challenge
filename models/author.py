from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        if not isinstance(id, int):
            raise TypeError("id must be an integer")
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("name must be a non-empty string")
        self._id = id
        self._name = name
        self.save()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def save(self):
        conn = get_db_connection()
        with conn:
            conn.execute("INSERT OR REPLACE INTO authors (id, name) VALUES (?, ?)", (self._id, self._name))

    def delete(self):
        conn = get_db_connection()
        with conn:
            conn.execute("DELETE FROM authors WHERE id = ?", (self._id,))
            conn.execute("DELETE FROM articles WHERE author_id = ?", (self._id,))

    def articles(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        return cur.fetchall()

    def magazines(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT magazines.name FROM magazines "
                    "JOIN articles ON magazines.id = articles.magazine_id "
                    "WHERE articles.author_id = ?", (self._id,))
        return [row["name"] for row in cur.fetchall()]
