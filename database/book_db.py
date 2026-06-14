from database.db_connection import connection


class BookDb:
    def __init__(self, db):
        self.db = db

    @property
    def connection(self):
        return self.db.get_connection()

    def create_book(self, data: dict):
        with self.connection.cursor(dictionary=True) as cursor:
            quary = """
            INSERT INTO books(title,author,genre)
            VALUES (%s,%s,%s)"""
            values = [data.get("title"), data.get("author"), data.get("genre")]
            cursor.execute(quary, values)
            self.connection.commit()

    def get_all_books(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()
            return books

    def get_book_by_id(self, id: int):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
            book = cursor.fetchone()
            return book

    def update_book(self, id: int, data: dict):
        with self.connection.cursor(dictionary=True) as cursor:
            set_parts = [f"{key} = %s" for key in data.keys()]
            set_clause = ", ".join(set_parts)

            quary = f"UPDATE books SET {set_clause} WHERE id = %s"
            values = list(data.values()) + [id]
            cursor.execute(quary, values)
            self.connection.commit()

    def set_available(self, id: int, val: bool, member_id: int):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(
                "UPDATE books SET is_available = %s, borrowed_by_member_id = %s WHERE id = %s",
                (val, member_id, id),
            )
            self.connection.commit()

    def count_total_books(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) AS total_books FROM books")
            count = cursor.fetchone()
            return count

    def count_available_books(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS available_books FROM books WHERE is_available = TRUE"
            )
            count = cursor.fetchone()
            return count

    def count_borrowed_books(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS borrowed_books FROM books WHERE is_available = FALSE"
            )
            count = cursor.fetchone()
            return count

    def count_by_genre(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT genre, COUNT(*) AS count FROM books GROUP BY genre")
            count = cursor.fetchall()
            return count

    def count_active_borrows_by_member(self, member_id: int):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM books WHERE borrowed_by_member_id = %s",
                (member_id,),
            )
            count = cursor.fetchone()[0]
            return count


books = BookDb(connection)
