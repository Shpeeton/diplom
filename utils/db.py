import pymysql
import pg8000

class Database:
    def __init__(self, db_type, config):
        self.db_type = db_type
        self.config = config
        self.connection = None

    def connect(self):
        if self.db_type == 'mysql':
            self.connection = pymysql.connect(**self.config)
        elif self.db_type == 'postgresql':
            self.connection = pg8000.connect(**self.config)

    def get_payment_status(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT status FROM payment_entity ORDER BY created DESC LIMIT 1")
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting payment status: {e}")
            return None

    def get_credit_status(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT status FROM credit_request_entity ORDER BY created DESC LIMIT 1")
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting credit status: {e}")
            return None

    def clear_all(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM payment_entity")
            cursor.execute("DELETE FROM credit_request_entity")
            cursor.execute("DELETE FROM order_entity")
            self.connection.commit()
        except Exception as e:
            print(f"Error clearing database: {e}")
            self.connection.rollback()