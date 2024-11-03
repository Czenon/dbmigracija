## REQUIREMENTS
1. Make sure Python is installed and is at least at version 3.12.2. The internal Python libraries have been tested with this version number.
2. Install PostgreSQL, version 16 is recommended
3. Install the psycopg2 library for Python, it allows connecting and executing DB queries in Python.
Use 'pip install psycopg2' in your command line. Make sure it's at least at version 2.9.10.
4. Launch Postgres server and change config.ini file with relevant DB info.

### USAGE
1. Run migration.py file first if you need to make a new DB and tables.
2. Run connect.py file to retrieve cat table info.