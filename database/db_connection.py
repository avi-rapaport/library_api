import mysql.connector


class DbConnection:
    def __init__(self):
        self.connect()

    def connect(self):
        self.connection = mysql.connector.connect(
            host="localhost", user="root", password="root", database="library_db"
        )

    def get_connection(self):
        if not self.connection.is_connected():
            self.connect()
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def create_tables(self):
        con = self.get_connection()
        with con.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS books(
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(50) NOT NULL,
            author VARCHAR(50) NOT NULL,
            genre ENUM('Fiction', 'Non-fiction', 'Science', 'History', 'Other') NOT NULL,
            is_available BOOLEAN DEFAULT TRUE NOT NULL,
            borrowed_by_member_id INT)
            """)
            con.commit()

            cursor.execute("""CREATE TABLE IF NOT EXISTS members(
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            is_active BOOLEAN DEFAULT TRUE NOT NULL,
            total_borrows INT NOT NULL DEFAULT 0)
            """)
            con.commit()


connection = DbConnection()
