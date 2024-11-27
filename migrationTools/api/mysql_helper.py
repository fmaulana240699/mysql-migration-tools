import mysql.connector

class mysqlHelper():
    def __init__(self, sql_commands, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.sql_commands = sql_commands

    def execute_query(self, batch_version):
        connection = None
        try:
            # Establish a connection to the MySQL server
            connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )

            if connection.is_connected():
                print("Connected to MySQL database")

            connection.start_transaction()
            cursor = connection.cursor(buffered=True)

            # Create migration table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_migration_version (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    batch_version VARCHAR(255)
                )
            """)

            # Execute SQL commands
            for result in cursor.execute(self.sql_commands, multi=True):
                if result.with_rows:
                    result.fetchall()

            # Insert or update the migration batch version
            cursor.execute("""
                INSERT INTO schema_migration_version (batch_version)
                VALUES (%s)
                ON DUPLICATE KEY UPDATE batch_version = VALUES(batch_version)
            """, (batch_version,))

            connection.commit()
            print("SQL commands executed successfully")

        except mysql.connector.Error as e:
            if connection:
                connection.rollback()
            print("Error:", e)
            raise

        finally:
            if connection and connection.is_connected():
                if 'cursor' in locals():
                    cursor.close()
                connection.close()
                print("MySQL connection closed")
