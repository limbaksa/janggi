import sqlite3
def makedb():
    conn = sqlite3.connect("./db/results.db")
    c=conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS game(
            gameid integer PRIMARY KEY,
            against TEXT,
            )""")
    conn.commit()
    conn.close()