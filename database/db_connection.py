import mysql.connector


def get_connection():
    connection = mysql.connector.connect(host="localhost", user="root", password="root")
    return connection


def create_tables():
    con = get_connection()
    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS library_db")
    cur.execute("USE library_db")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS books(
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(50) NOT NULL,
    author VARCHAR(50) NOT NULL,
    genre ENUM('fiction', 'non-fiction', 'science', 'history', 'other') NOT NULL,
    is_available BOOLEAN DEFAULT TRUE NOT NULL,
    borrowed_by_member_id INT)
    """)
    con.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS members(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    total_borrows INT NOT NULL)
    """)
    con.commit()
