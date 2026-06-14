from db_connection import connection


class MemberDb:
    def __init__(self, db):
        self.db = db

    @property
    def connection(self):
        return self.db.get_connection()

    def create_member(self, data: dict):
        with self.connection.cursor(dictionary=True) as cursor:
            quary = """
            INSERT INTO members(name,email)
            VALUES (%s,%s)"""
            values = [data.get("name"), data.get("email")]
            cursor.execute(quary, values)
            self.connection.commit()

    def get_all_members(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM members")
            members = cursor.fetchall()
            return members

    def get_member_by_id(self, id: int):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
            member = cursor.fetchone()
            return member

    def update_member(self, id: int, data: dict):
        with self.connection.cursor(dictionary=True) as cursor:
            set_parts = [f"{key} = %s" for key in data.keys()]
            set_clause = ", ".join(set_parts)

            quary = f"UPDATE members SET {set_clause} WHERE id = %s"
            values = list(data.values()) + [id]
            cursor.execute(quary, values)
            self.connection.commit()

    def deactivate_member(self, id):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("UPDATE members SET is_active = False WHERE id = %s", (id,))
            self.connection.commit()

    def activate_member(self, id):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("UPDATE members SET is_active = True WHERE id = %s", (id,))
            self.connection.commit()

    def increment_borrows(self, id):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(
                "UPDATE members SET total_borrows = total_borrows + 1 WHERE id = %s",
                (id,),
            )
            self.connection.commit()

    def count_active_members(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS active_members FROM members WHERE is_active = True"
            )
            count = cursor.fetchone()
            return count

    def get_top_member(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM members ORDER BY total_borrows DESC LIMIT 1")
            top = cursor.fetchone()
            return top


members = MemberDb(connection)
