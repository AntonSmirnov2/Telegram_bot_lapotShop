import sqlite3

DB_NAME = 'lapotshop.sqlite'

connect = sqlite3.connect(DB_NAME)
cursor = connect.cursor()

cursor.execute("""SELECT * FROM user;""")
a = cursor.fetchall()
connect.close()

for i in a:
    print(i)
