import psycopg2
import datetime
from configparser import ConfigParser

# Retrieve login data from config
config = ConfigParser()
config.read('config.ini')

dbname = config.get('postgres_config', 'database')
dbaddress = config.get('postgres_config', 'address')
dbport = config.get('postgres_config', 'port')
dbusername = config.get('postgres_config', 'username')
dbuserpass = config.get('postgres_config', 'password')

dt = datetime.datetime.now()
request_date = str(dt.year) + "-" + str(dt.month).zfill(2) + "-" + str(dt.day).zfill(2)
request_time = str(dt.hour) + str(dt.minute) + str(dt.second)
print(request_date)
print(request_time)

def connect(name, address, port, username, userpass):
    with psycopg2.connect(f"dbname={name} user={username} password={userpass} host={address} port={port}") as conn:
        return conn

# Create a DB connection using config file parameters    
conn = connect(dbname, dbaddress, dbport, dbusername, dbuserpass)

# Create a new cursor for retrieving data from DB
cur = conn.cursor()

# Select name and age for all cats in DB, then each row into a tuple
cur.execute("SELECT name, age FROM cats")
data = cur.fetchall()

# Print out data if our rows actually contain something
while data is not None:
    for row in data:
        print(f"Name: {row[0]} | Age: {row[1]}")