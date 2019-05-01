import unittest
import os
import io
import sys
from database_exercise import *

class TestDatabase(unittest.TestCase):
    """
    Class dedicated to unit testing our database functions.
    :attr connection: connection to test database.
    :attr cursor: connection's Cursor object.
    """
    
    connection = None
    cursor = None

    @classmethod
    def setUpClass(cls):
        """
        Set up temporary database, unittestdb.db.
        """
        cls.connection = sqlite3.connect("unittestdb.db")
        cls.cursor = cls.connection.cursor()
    
        # create person table and insert data
        cls.cursor.execute("""
            CREATE TABLE people
            (id text, first_name text, last_name text)""")
        people = [("1", "Joe", 'Smith'),
                  ("2", "Bob", 'Smith'),
                  ("3", "Matt", 'Smith')]
        cls.cursor.executemany("""
            INSERT INTO people 
            VALUES (?,?,?)""", people)
        
        #create visits table and insert data
        cls.cursor.execute("""
            CREATE TABLE visits
            (personId text, siteId text, time_visited text)""")
        visits = [("1","1","2005-08-23 03:52:02"),
                  ("1","2","2005-08-23 04:52:02"),
                  ("1","3","2005-08-23 05:52:02"),
                  ("2","1","2005-08-23 03:52:02"),
                  ("2","2","2005-08-23 04:52:02"),
                  ("3","1","2005-08-23 03:52:02")]
        cls.cursor.executemany("""
            INSERT INTO visits 
            VALUES (?,?,?)""", visits)
        
        # create frequent_browsers table
        cls.cursor.execute("""
            CREATE TABLE frequent_browsers
            (person_id text, num_sites_visited text)""")
 
        # save data to database
        cls.connection.commit()
 
    @classmethod
    def tearDownClass(cls):
        """
        Delete our database file.
        """
        os.remove("unittestdb.db")
    
    def test_create_connection(self):
        """
        Test our connection to the database.
        """
        actual = self.connection

        self.assertNotEqual(actual, None)
        
        
    def test_select_most_visited_sites(self):
        """
        Tests if our query joins tables and counts number of sites correctly.
        """
        actual = select_most_visited_sites(self.connection, '10')
        expected = [("1", 3),
                 ("2", 2),
                 ("3", 1)]

        self.assertEqual(actual, expected)
        
    
    def test_insert_frequent_browsers(self):
        """
        Tests inserting into our frequent_browsers table.
        """
        expected = [("1", "3"),
                 ("2", "2"),
                 ("3", "1")]
        insert_frequent_browsers(self.connection, expected)
        actual = self.cursor.execute("SELECT * FROM frequent_browsers").fetchall()
        
        self.assertEqual(actual, expected)
    
    def test_select_all_frequent_browsers(self):
        """
        Tests selecting all from our frequent_browsers table.
        """
        actual = select_all_frequent_browsers(self.connection)
        expected = [("1", "3"),
                 ("2", "2"),
                 ("3", "1")]
        
        self.assertEqual(actual, expected)
    
    def test_print_query(self):
        """
        Tests print query results.
        """
        actual = io.StringIO()

        # redirecting stdout
        sys.stdout = actual

        query = [("1", "3"),
                 ("2", "2"),
                 ("3", "1"),]
        print_query(query)

        # reset redirection
        sys.stdout = sys.__stdout__  
        
        expected = "('1', '3')\n('2', '2')\n('3', '1')\n"

        self.assertEqual(expected, actual.getvalue())
        
        
    