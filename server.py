import socket
import sqlite3


def rglob(data):
    sql = sqlite3.connect("user.db")
    c = sql.cursor()
    c.execute("SELECT * FROM scores ORDER BY score DESC")
    return "1," + str(c.fetchmany(5))


def rloc(data):
    sql = sqlite3.connect("user.db")
    c = sql.cursor()
    c.execute("SELECT * FROM scores WHERE username=? ORDER BY score DESC", (data,))
    sent = str(c.fetchmany(5))
    return "1," + sent


def reg(data):
    data = data.split(".")
    sql = sqlite3.connect("user.db")
    c = sql.cursor()
    c.execute("INSERT INTO scores (username, score) VALUES(?, ?)", (data[0], data[1]))
    sql.commit()
    sql.close()
    return "1"


def sq(data):
    data = data.split(".")
    sql = sqlite3.connect("user.db")
    c = sql.cursor()
    c.execute("SELECT sq FROM users WHERE username=?", (data[0],))
    search = c.fetchone()
    if search != None:
        return "1," + search[0]
    else:
        return "0"


def fp(data):
    data = data.split(".")
    sql = sqlite3.connect("user.db")
    c = sql.cursor()
    c.execute("SELECT password FROM users WHERE username=? AND sa=?", (data[0], data[1]))
    search = c.fetchone()
    if search != None:
        return "1," + search[0]
    else:
        return "0"


def ca(data):
    data = data.split(".")
    sql = sqlite3.connect("user.db")
    c = sql.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (data[0],))
    if len(c.fetchall()) == 0 and len(data[0]) != 0 and len(data[1]) != 0 and len(data[2]) != 0 and len(data[3]) != 0:
        c.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (data[0], data[1], data[2], data[3]))
    else:
        sql.commit()
        sql.close()
        return "0"
    sql.commit()
    sql.close()
    return "1"


def login(data):
    data = data.split(".")
    sql = sqlite3.connect("user.db")
    c = sql.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password =?", (data[0], data[1]))
    if len(c.fetchall()) == 1:
        return "1"
    else:
        return "0"

def process(data):
    data = data.split(",")
    return str(globals()[data[0]](data[1]))


def listener():
    host = "127.0.0.1"
    port = 5000
    Listener = socket.socket()
    Listener.bind((host, port))
    while True:
        Listener.listen(1)
        conn, addr = Listener.accept()
        data = conn.recv(2048).decode()
        conn.send(process(data).encode())
        conn.close()

listener()
