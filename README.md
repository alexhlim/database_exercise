# Database Exercise

## Database Contents

### Tables
1. people (id text, first_name text, last_name text)
2. sqlite_sequence (name text, seq text)
3. sites (id text, url text)
4. visits (personId text, siteId text, time_visited text)
5. frequent_browsers (person_id text, num_sites_visited text)

## Goal

Given a test database (testdb.db), my goal is to achieve the following:

1. Find the ten people who have visited the most sites
2. List these people in descending order of the number of sites they've visited in a table called frequent_browsers

## Running the Program

I ran the program using ```Python 3.7.0```.

To execute the main program, execute the following on your command line:

```python database_exercise.py```

To perform unittests, execute the following on your command line:

```python -m unittest database_exercise_unittests.py```
