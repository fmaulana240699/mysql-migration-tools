import mysql.connector

# Function to read SQL file
def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        sql_commands = file.read()
    return sql_commands

# Function to execute SQL commands
def execute_sql_commands(sql_commands, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(sql_commands, multi=True)
        print("SQL commands executed successfully")
    except mysql.connector.Error as e:
        print("Error executing SQL commands:", e)
    finally:
        cursor.close()

# MySQL connection parameters
host = "localhost"
username = "your_username"
password = "your_password"
database = "your_database"

# Path to your SQL file
sql_file_path = "/path/to/your/file.sql"

try:
    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )

    # Check if the connection was successful
    if connection.is_connected():
        print("Connected to MySQL database")

    # Read SQL commands from the file
    sql_commands = read_sql_file(sql_file_path)

    # Execute SQL commands
    execute_sql_commands(sql_commands, connection)

except mysql.connector.Error as e:
    print("Error connecting to MySQL:", e)

finally:
    # Close the connection
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("MySQL connection closed")
