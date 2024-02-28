import mysql.connector

class mysqlHelper():
    def __init__(self, sql_commands):
        self.host = "localhost"
        self.username = "fmaulana"
        self.password = "jaringan"
        self.database = "testing"
        self.sql_commands = sql_commands

    def execute_query(self):
        try:
            # Establish a connection to the MySQL server
            connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )

            # Check if the connection was successful
            if connection.is_connected():
                print("Connected to MySQL database")

                try:
                    cursor = connection.cursor(buffered=True)
                    cursor.execute(self.sql_commands, multi=True)
                    print("SQL commands executed successfully")
                except mysql.connector.Error as e:
                    print("Error executing SQL commands:", e)
                finally:
                    cursor.close()  

        except mysql.connector.Error as e:
            print("Error connecting to MySQL:", e)

        finally:
            # Close the connection
            if 'connection' in locals() and connection.is_connected():
                connection.close()
                print("MySQL connection closed")


# test = mysqlHelper("select * from my_table")
# test.execute_query()