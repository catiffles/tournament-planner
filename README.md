#Tournament Results

###Summary
A database schema that stores game matches and python code to determine the winners of various games.

###Contents
-tournament.py: Python code that uses the database to run a Swiss Pairing tournament
-tournament.sql: SQL file that defines the parameters of the database
-tournament_test.py: Test conditions provided by Udacity to test tournament.py

###How to run
- Clone this repo
- Navigate to the repo in terminal
- Type psql to enter sql console
- Type \i tournament.sql to run tournament.sql file and create tables.
-Exit out of sql console with the command \q
- Run python tournament_test.py to check for passing tests.
