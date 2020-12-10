import sqlite3

conn = sqlite3.connect('mvrulz.db')

conn.execute('''CREATE TABLE TELUGU_MOVIE_LINKS 
		(TITLE TEXT PRIMARY KEY NOT NULL,
		LINK TEXT NOT NULL)''')

print('Table TELUGU_MOVIE_LINKS Created')

conn.close()

