import json
import sqlite3


def get_connect():
    return sqlite3.connect('mock.db')


# noinspection PyShadowingBuiltins
class Database:
    def __init__(self):
        con = get_connect()
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS RESOURCES(ID, PAYLOAD)')
        con.close()

    def save(self, id, payload):
        con = get_connect()
        cur = con.cursor()
        if isinstance(payload, bytes):
            json_str = payload.decode('utf-8')
        elif isinstance(payload, str):
            json_str = payload
        else:
            json_str = json.dumps(payload)

        if self.exist(id):
            cur.execute('UPDATE RESOURCES SET PAYLOAD = ? WHERE ID = ?', (json_str, id.lower()))
        else:
            cur.execute('INSERT INTO RESOURCES(ID, PAYLOAD) VALUES(?,?)', (id.lower(), json_str))

        con.commit()
        con.close()

    def exist(self, id):
        con = get_connect()
        cur = con.cursor()
        res = cur.execute('SELECT ID FROM RESOURCES WHERE ID = ?', (id.lower(),))
        flag = res.fetchone() is not None
        con.close()
        return flag

    def get(self, id):
        con = get_connect()
        cur = con.cursor()
        res = cur.execute('SELECT PAYLOAD FROM RESOURCES WHERE ID = ?', (id.lower(),))
        payload = json.loads(res.fetchone()[0])
        con.close()
        return payload

    def query(self, id):
        with get_connect() as con:
            cur = con.cursor()
            res = cur.execute('SELECT ID, PAYLOAD FROM RESOURCES WHERE ID LIKE ?', (f'{id.lower()}/%',))
            return res.fetchall()

    def delete(self, id):
        with get_connect() as con:
            cur = con.cursor()
            cur.execute('DELETE FROM RESOURCES WHERE ID = ?', (id.lower(),))
