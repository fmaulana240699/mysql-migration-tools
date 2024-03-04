import mysql.connector

class mysqlHelper():
    def __init__(self, sql_commands, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.sql_commands = sql_commands

    def execute_query(self, batch_version):
        try:
            # Establish a connection to the MySQL server
            connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )

            connection.start_transaction()

            # Check if the connection was successful
            if connection.is_connected():
                print("Connected to MySQL database")

                try:
                    #### create table migration on target db if not exist ####
                    cursor = connection.cursor(buffered=True)
                    cursor.execute("CREATE TABLE IF NOT EXISTS schema_migration_version (id INT AUTO_INCREMENT PRIMARY KEY, batch_version VARCHAR(255))")

                    cursor.execute(self.sql_commands, multi=True)
                   
                    #### update migration batch version ####
                    cursor.execute("INSERT INTO schema_migration_version (batch_version) VALUES (%s) ON DUPLICATE KEY UPDATE batch_version = VALUES(batch_version)", (batch_version,))

                    print("SQL commands executed successfully")
                except mysql.connector.Error as e:
                    connection.rollback()
                    print("Error executing SQL commands:", e)
                    raise Exception("Error executing SQL commands: " + str(e))
                finally:
                    cursor.close()  

        except mysql.connector.Error as e:
            print("Error connecting to MySQL:", e)
            raise Exception("Error connecting to MySQL: " + str(e))

        finally:
            # Close the connection
            if 'connection' in locals() and connection.is_connected():
                connection.commit()
                connection.close()
                print("MySQL connection closed")