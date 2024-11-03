import psycopg2
import datetime
import os
import time

from configparser import ConfigParser
from connect import connect

# Get config values
config = ConfigParser()
config.read('config.ini')

print("confs")
dbname = config.get('postgres_config', 'database')
dbaddress = config.get('postgres_config', 'address')
dbport = config.get('postgres_config', 'port')
dbusername = config.get('postgres_config', 'username')
dbuserpass = config.get('postgres_config', 'password')

# Connect to DB using the method in connect.py and return connection object
print("guh")
conn = connect(dbname, dbaddress, dbport, dbusername, dbuserpass)
print("guh2")
# Make a DB cursor
cur = conn.cursor()

# Create migrations table
def make_migrations_table():
    result = cur.execute('''
    CREATE TABLE public.migrations
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

# Get all migration files
migrations_list = []
cur_dir = os.getcwd()
migrations_file_list = os.listdir(cur_dir + "/migrations/")
for filename in migrations_file_list:
    if filename.endswith('.sql'):
        migrations_list.append(filename)

# Sort migration files in correct date order
migrations_list.sort(reverse=False)

# Counter for how many migration actions we do
counter = 0

make_migrations_table()

for migration in migrations_list:
    with open(cur_dir + "/migrations/" + migration, 'r') as file:
        migration_sql = file.read()
        mig_exec_ts = int(time.time())
        mig_exec_td = datetime.datetime.utcfromtimestamp(mig_exec_ts).strftime('%Y-%m-%d %H:%M:%S')
        migration_value_insert(migration, mig_exec_ts, mig_exec_td)
        counter += 1

if counter == 0:
    print("No migrations to execute.")