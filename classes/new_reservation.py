import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('reservations.db')
cursor = conn.cursor()

# Create a table to store reservations
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY,
        restaurant_name TEXT,
        max_party_size INTEGER,
        current_bid INTEGER,
        neighborhood TEXT
    )
''')

# Prompt the user to post reservations
while True:
    restaurant_name = input("Enter the restaurant name (or 'exit' to finish): ")
    
    if restaurant_name.lower() == 'exit':
        break
    
    max_party_size = int(input("Enter the max party size: "))
    current_bid = int(input("Enter the current bid: "))
    neighborhood = input("Enter the neighborhood: ")

    # Insert data into the table
    cursor.execute('''
        INSERT INTO reservations (restaurant_name, max_party_size, current_bid, neighborhood)
        VALUES (?, ?, ?, ?)
    ''', (restaurant_name, max_party_size, current_bid, neighborhood))

# Commit the changes and close the connection
conn.commit()
conn.close()
