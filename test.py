import re

# Sample string
string = "migrations-data/2024-02-18-0001-createTableTesting.sql"

# Regular expression pattern to match the desired part
pattern = r'\d{4}-\d{2}-\d{2}-\d{3}'

# Extract the matching part
match = re.search(pattern, string)

