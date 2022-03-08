import sqlite3

with open('schema.sql') as f:
  s = f.read()

with sqlite3.connect("database.db") as con:
  con.executescript(s)