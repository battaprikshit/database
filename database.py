import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def execute_query(self, query, parameters=None):
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return False

    def fetch_data(self, query, parameters=None):
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return []

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        return self.execute_query(query)

    def insert_data(self, table_name, values):
        placeholders = ",".join(["?" for _ in range(len(values))])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        return self.execute_query(query, values)

    def select_data(self, table_name, columns="*", condition=None):
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        return self.fetch_data(query)

    def update_data(self, table_name, column, value, condition=None):
        query = f"UPDATE {table_name} SET {column} = ?"
        if condition:
            query += f" WHERE {condition}"
        return self.execute_query(query, (value,))

    def delete_data(self, table_name, condition=None):
        query = f"DELETE FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        return self.execute_query(query)

def main():
    
# Create an instance of the Database class
    db = Database("mydatabase.db")

    # Connect to the database
    db.connect()

    # Create a table
    db.create_table("users", "id INTEGER PRIMARY KEY, name TEXT, age INTEGER")

    # Insert data into the table
    db.insert_data("users", (1, "John Doe", 25))
    db.insert_data("users", (2, "Jane Smith", 30))
    db.insert_data("users", (3, "Prikshit", 26))
    db.insert_data("users", (4, "Kartik", 28))

    # Select data from the table
    data = db.select_data("users", "*", "age > 25")
    for row in data:
        print(row)

    # Update data in the table
    db.update_data("users", "age", 26, "name = 'John Doe'")

    # Delete data from the table
    db.delete_data("users", "age <= 26")

    # Disconnect from the database
    db.disconnect()

if __name__ == "__main__":
    main()
