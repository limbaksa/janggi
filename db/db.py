import sqlite3
def makedb():
    conn = sqlite3.connect("./db/results.db")
    c=conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS game(
            gameid integer PRIMARY KEY AUTOINCREMENT,
            cho TEXT,
            han TEXT,
            moves integer,
            result TEXT,
            record TEXT
            )""")
    conn.commit()
    conn.close()

def add_game(cho,han,moves,result,record):
    conn = sqlite3.connect("./db/results.db")
    c=conn.cursor()
    c.execute("INSERT INTO game VALUES (null,?,?,?,?,?)",(cho,han,moves,result,record))
    conn.commit()
    conn.close()