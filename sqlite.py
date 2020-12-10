import sqlite3

conn = sqlite3.connect('mvrulz.db')

print('Successfully Connected')
conn.close()
