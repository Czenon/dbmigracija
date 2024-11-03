import psycopg2
import time
import logging
import os

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
logging.basicConfig(filename='logs/connect.log', level=logging.INFO)
logger.info("Started at " + exec_td)

# Retrieve login data from config
config = ConfigParser()
logger.info("Reading config.ini file...")
config.read('config.ini')

dbname     = config.get('postgres_config', 'database')
dbaddress  = config.get('postgres_config', 'address')
dbport     = config.get('postgres_config', 'port')
dbusername = config.get('postgres_config', 'username')
dbuserpass = config.get('postgres_config', 'password')

# Use config file data to connect to DB
def connect(name, address, port, username, userpass):
    with psycopg2.connect(f"dbname={name} user={username} password={userpass} host={address} port={port}") as conn:
        return conn

# Create a DB connection using config file parameters
logger.info("Connecting to database...")
conn = connect(dbname, dbaddress, dbport, dbusername, dbuserpass)

# Create a new cursor for retrieving data from DB
logger.info("Creating cursor...")
cur = conn.cursor()

# Select name and age for all cats in DB, then each row into a tuple
logger.info("Querying cat name and age...")
cur.execute("SELECT name, age FROM cats")
data = cur.fetchall()

# Print out data if our rows actually contain something
logger.info("Printing cat data...")
if data is not None:
    for row in data:
        print(f"Name: {row[0]} | Age: {row[1]}")

logger.info("Finished.")
conn.close()