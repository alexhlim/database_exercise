import sqlite3 
from sqlite3 import Error

def create_connection(db_file):
    """
    Create connection to SQLite database via db_file.
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return None

def select_most_visited_sites(connection, num_rows):
    """
    Query how many sites each person visited and
    display the top num_rows amount.
    :param connection: connection to database
    :param num_rows: number of rows to display
    :return: list of rows
    """
    cursor = connection.cursor()
    sql= """
        SELECT P.id, COUNT(*) AS total_visits 
        FROM people AS P 
        JOIN visits AS V 
            ON P.id = V.personId 
        GROUP BY P.id 
        ORDER BY total_visits DESC
        LIMIT ?"""
    args = (num_rows,)
    cursor.execute(sql, args)
    rows = cursor.fetchall()
    return rows

def insert_frequent_browsers(connection, rows):
    """
    Insert new rows into the frequent_browsers table.
    :param connection: connection to database
    :param rows: list of rows to insert with the form [(person_id, num_sites_visited)]
    :return:
    """
    cursor = connection.cursor()
    sql = """
        INSERT INTO frequent_browsers (person_id, num_sites_visited)
        VALUES (?,?)"""
    args = rows
    cursor.executemany(sql, args)
    

def select_all_frequent_browsers(connection):
    """
    Query all rows in frequent_browsers.
    :param connection: connection to database
    :return: list of rows
    """
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM frequent_browsers")
    rows = cursor.fetchall()
    return rows
    
def print_query(query):
    """
    Print out rows from a list object.
    :param query: list of rows
    :return:
    """
    for row in query:
        print(row)

def main():
    db = "testdb.db"
    connection = create_connection(db)
    with connection:
        cursor = connection.cursor()
        
        # query top 10 people with most visited sites
        rows = select_most_visited_sites(connection, 10)
        
        # insert rows into frequent_browsers table
        insert_frequent_browsers(connection, rows)
        
        # display contents in frequent_browsers
        freq_browsers = select_all_frequent_browsers(connection)
        print("frequent_browsers table:")
        print_query(freq_browsers)
        connection.commit()
        
    cursor.close()
    connection.close()

if __name__ == '__main__':
    main()