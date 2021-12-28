import sqlite3

conn = sqlite3.connect("./accounts.db")
cur = conn.cursor()
# pylint: disable=W1514
with open('schema.sql') as schema:
    cur.executescript(schema.read())
conn.commit()
