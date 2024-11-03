import psycopg2
import logging
import os
import time

from datetime import datetime
from configparser import ConfigParser

# Get program execution time to use in logger file
exec_ts = int(time.time())
exec_td = datetime.fromtimestamp(exec_ts).strftime('%Y-%m-%d %H:%M:%S')

# Get working directory and create logger
cur_dir = os.getcwd()
logger = logging.getLogger()

# Make log folder if it does not exist already
if not os.path.exists(cur_dir + '/logs'): 
    os.makedirs('logs')
logging.basicConfig(filename='logs/migration.log', level=logging.INFO)
logger.info("Started at " + exec_td)

# Get config values
logger.info("Reading config.ini file...")
config = ConfigParser()
config.read('config.ini')

dbname     = config.get('postgres_config', 'database')
dbaddress  = config.get('postgres_config', 'address')
dbport     = config.get('postgres_config', 'port')
dbusername = config.get('postgres_config', 'username')
dbuserpass = config.get('postgres_config', 'password')

# Connect to Postgres DB and return a connection object
def connect(name, address, port, username, userpass):
    with psycopg2.connect(f"dbname={name} user={username} password={userpass} host={address} port={port}") as conn:
        return conn

# Connect to DB using the method in connect.py and return connection object
logger.info("Connecting to DB...")
conn = connect(dbname, dbaddress, dbport, dbusername, dbuserpass)

# Make a DB cursor
cur = conn.cursor()

# Execute SQL queries
def exec_sql(query):
    status = 0
    try:
        cur.execute(query)
        conn.commit()
    except:
        status = 1
        pass
    return status

# Create migrations table if it does not exist yet
def make_migrations_table():
    result = cur.execute('''
    CREATE TABLE IF NOT EXISTS public.migrations
    (
    id serial NOT NULL,
    name character varying(255),
    exec_ts integer,
    exec_td character varying(20),
    PRIMARY KEY (id)
    );

    ALTER TABLE IF EXISTS public.migrations
    OWNER to postgres;''')
    conn.commit()

    return result

# Populate migrations table
def migration_value_insert(name, exec_ts, exec_td):
    cur.execute(f"INSERT INTO public.migrations (name, exec_ts, exec_td) VALUES ('{str(name)}', '{str(exec_ts)}', '{str(exec_td)}');")
    conn.commit()

# Get all migration files
logger.info("Checking for migration files...")
migrations_list = []
migrations_file_list = os.listdir(cur_dir + "/migrations/")
for filename in migrations_file_list:
    if filename.endswith('.sql'):
        migrations_list.append(filename)

# Sort migration files in correct date order
logger.info("Sorting migration files by date...")
migrations_list.sort(reverse=False)

# Counter for how many migration actions we do
counter = 0

logger.info("Creating migrations table...")
make_migrations_table()

logger.info("Processing migration files...")
for migration in migrations_list:
    with open(cur_dir + "/migrations/" + migration, 'r') as file:
        migration_sql = file.read()
        logger.info("Attempting to execute migration SQL code...")
        if exec_sql(migration_sql) == 0:
            logger.info("Writing migration execution success data to database...")
            mig_exec_ts = int(time.time())
            mig_exec_td = datetime.fromtimestamp(mig_exec_ts).strftime('%Y-%m-%d %H:%M:%S')
            migration_value_insert(migration, mig_exec_ts, mig_exec_td)
            counter += 1
        else:
            logger.info("Migration file " + migration + " failed! Aborting.")
            break

if counter == 0:
    logger.info("No migrations to execute.")

conn.close()
logger.info("Done.")