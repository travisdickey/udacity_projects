#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' writes ways_nodes csv to ways_nodes sql table '''

import sqlite3
import csv
from pprint import pprint
# modified from code posted to Udacity forums

sqlite_file = 'osm.db'    # name of the sqlite database file

# Connect to the database
conn = sqlite3.connect(sqlite_file)
# Get a cursor object
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS ways_nodes''')
conn.commit()
# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE ways_nodes (
        id INTEGER NOT NULL,
        node_id INTEGER NOT NULL,
        position INTEGER NOT NULL,
        FOREIGN KEY (id) REFERENCES ways(id),
        FOREIGN KEY (node_id) REFERENCES nodes(id)
        );
    ''')
# commit the changes
conn.commit()
# Read in the csv file as a dictionary, format the
# data as a list of tuples:
with open('ways_nodes.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['node_id'].decode("utf-8"), i['position'].decode("utf-8")) for i in dr]
# insert the formatted data
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_db)
# commit the changes
conn.commit()
cur.execute('SELECT * FROM ways_nodes')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)
conn.close()
