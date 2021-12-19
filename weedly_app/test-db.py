import psycopg2
from urllib.parse import urlparse
from fuzzywuzzy import process
from datetime import datetime

MOI_ID = 106441967
from psycopg2.extras import LoggingConnection
import pandas as pd
import logging

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s',) # filename='my_final.log'
# logger = logging.getLogger('bd.py')
# logger.setLevel(logging.DEBUG)

'''1. подключаемся к БД'''
result = urlparse("postgres://bimivwpixxvonl:4aac875184f3b2d548deac99e8406326ca56b5e63e7708a18509ad2b7204f2da@ec2-35-169-204-98.compute-1.amazonaws.com:5432/d6sqr5qhk9amgn")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port
conn = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=hostname,
    port=port
)
cur = conn.cursor()


def get_all_media():
    cur.execute(f'''select source_name from user_table_1''')
    return set([e[-1] for e in cur.fetchall()])

def get_all_links():
    cur.execute(f'''select link from user_table_1''')
    return set([e[-1] for e in cur.fetchall()])


#print(get_all_links())

