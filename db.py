import sqlite3


def db_start():
    # Start an SQLite DB in memory
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()

    # Creates tables if they doesn't exists
    c.execute("""CREATE TABLE IF NOT EXISTS auctions (auc int, item int, owner varchar(30), buyout int, quantity int)""")
    c.execute("""CREATE TABLE IF NOT EXISTS marketvalue (item int, marketvalue varchar(255), quantity int)""")
    c.execute("""CREATE TABLE IF NOT EXISTS status (last_update int, region varchar(10), realm varchar(30))""")

    conn.commit()
    return conn
