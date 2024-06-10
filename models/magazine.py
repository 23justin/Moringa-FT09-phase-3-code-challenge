from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        if not isinstance(id, int):
            raise TypeError("id must be an integer")
        if not isinstance(name, str) or len(name) < 2 or len(name) > 16:
            raise ValueError("name must be a string between 2 and 16 characters")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("category must be a non-empty string")
        self._id = id
        self._name = name
        self._category = category
        self.save()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def save(self):
        conn = get_db_connection()
        with conn:
            conn.execute("INSERT OR REPLACE INTO magazines (id, name, category) VALUES (?, ?, ?)", (self._id, self._name, self._category))

    def delete(self):
        conn = get_db_connection()
        with conn:
            conn.execute("DELETE FROM magazines WHERE id = ?", (self._id,))
            conn.execute("DELETE FROM articles WHERE magazine_id = ?", (self._id,))

    def articles(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE magazine_id = ?", (self._id,))
        return cur.fetchall()

    def contributors(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT authors.name FROM authors "
                    "JOIN articles ON authors.id = articles.author_id "
                    "WHERE articles.magazine_id = ?", (self._id,))
        return [row["name"] for row in cur.fetchall()]

    def article_titles(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT title FROM articles WHERE magazine_id = ?", (self._id,))
        titles = [row["title"] for row in cur.fetchall()]
        return titles if titles else None

    def contributing_authors(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT authors.* FROM authors "
                    "JOIN articles ON authors.id = articles.author_id "
                    "WHERE articles.magazine_id = ? "
                    "GROUP BY authors.id "
                    "HAVING COUNT(articles.id) > 2", (self._id,))
        return cur.fetchall()
